#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Pipeline OCR con matching por palabras clave.

Fase actual: PDF -> imagen -> OCR -> matching por etiquetas -> JSON.

Uso:
    python scripts/ocr.py <ruta_al_pdf> [dpi]

Salida:
    - Imprime por stdout un JSON con el contrato de DATA_MODEL.md.
    - Guarda la imagen en recursos/salida/<nombre_pdf>_p1.png
"""

import json
import math
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_LIBS = _HERE.parent / "recursos" / "libs"
if str(_LIBS) not in sys.path:
    sys.path.insert(0, str(_LIBS))

import pypdfium2 as pdfium

_PADDLE_OCR_JSON = _HERE.parent / "recursos" / "paddleocr-json" / "PaddleOCR-json.exe"

# ---------------------------------------------------------------------------
# Normalización de texto
# ---------------------------------------------------------------------------

def normalizar(texto: str) -> str:
    """Minúsculas, sin tildes, sin paréntesis, espacios colapsados."""
    if not texto:
        return ""
    texto = texto.lower()
    # Quitar tildes/diacríticos
    texto = "".join(
        c for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )
    # Quitar paréntesis y signos de puntuación frecuentes
    for ch in "()[]{}.,;:·-–—/\\":
        texto = texto.replace(ch, " ")
    # Colapsar espacios
    texto = " ".join(texto.split())
    return texto


def levenshtein(a: str, b: str) -> int:
    """Distancia de Levenshtein estándar."""
    if len(a) < len(b):
        return levenshtein(b, a)
    if not b:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, start=1):
        curr = [i]
        for j, cb in enumerate(b, start=1):
            cost = 0 if ca == cb else 1
            curr.append(min(
                curr[j - 1] + 1,      # inserción
                prev[j] + 1,          # borrado
                prev[j - 1] + cost,   # substitución
            ))
        prev = curr
    return prev[-1]


def similitud(a: str, b: str) -> float:
    """Similitud normalizada 0.0-1.0 basada en Levenshtein."""
    if not a or not b:
        return 0.0
    return 1.0 - levenshtein(a, b) / max(len(a), len(b))


# ---------------------------------------------------------------------------
# Catálogo territorial (matching por niveles con códigos INE)
# ---------------------------------------------------------------------------

CATALOGO_PATH = _HERE.parent / "recursos" / "catalogo-hovaes-lugares-galicia-completo.json"

PROVINCIA_NOMBRE_POR_CODIGO = {
    "15": "Coruña (A)",
    "27": "Lugo",
    "32": "Ourense",
    "36": "Pontevedra",
}

UMBRAL_ACEPTAR_CONCELLO = 0.80
UMBRAL_ACEPTAR_LOCALIDADE = 0.80
UMBRAL_ACEPTAR_LUGAR = 0.80

_CATALOGO_CACHE = None


def cargar_catalogo(path=CATALOGO_PATH):
    """Carga el catálogo territorial con UTF-8 explícito (sin BOM)."""
    global _CATALOGO_CACHE
    if _CATALOGO_CACHE is None:
        with open(path, "r", encoding="utf-8") as f:
            _CATALOGO_CACHE = json.load(f)
    return _CATALOGO_CACHE


def normalizar_para_catalogo(texto: str) -> str:
    """Igual que normalizar(): minúsculas, sin tildes, espacios colapsados."""
    return normalizar(texto)


def _nombre_provincia(codigo_concello: str):
    """Devuelve {codigo, nome} de la provincia a partir de los 2 primeros dígitos del concello."""
    codigo = codigo_concello[:2]
    nombre = PROVINCIA_NOMBRE_POR_CODIGO.get(codigo)
    if nombre is None:
        return None
    return {"codigo": codigo, "nome": nombre}


def _items_concellos(catalogo):
    items = []
    for concellos in catalogo.values():
        for nombre, datos in concellos.items():
            items.append((nombre, datos["codigo"]))
    return items


def _items_localidades(catalogo, codigo_concello):
    items = []
    for concellos in catalogo.values():
        for datos in concellos.values():
            if datos["codigo"] != codigo_concello:
                continue
            for nombre, datos_loc in datos["localidades"].items():
                items.append((nombre, datos_loc["codigo"]))
            return items
    return items


def _items_lugares(catalogo, codigo_localidade):
    items = []
    for concellos in catalogo.values():
        for datos in concellos.values():
            for datos_loc in datos["localidades"].values():
                if datos_loc["codigo"] != codigo_localidade:
                    continue
                for lugar in datos_loc["lugares"]:
                    items.append((lugar["nome"], lugar["codigo"]))
                return items
    return items


def aplicar_matching_territorial(campos, catalogo):
    matching = {
        "provincia": None,
        "concello": None,
        "localidade": None,
        "lugar": None,
        "match_confidence": 0.0,
        "candidates": [],
    }
    scores_aceptados = []
    valor_concello = _valor_campo(campos, "concello")
    concello_aceptado = None
    if valor_concello:
        candidatos_concello = buscar_en_catalogo(catalogo, valor_concello, "concello")
        if candidatos_concello:
            mejor = candidatos_concello[0]
            if mejor["score"] >= UMBRAL_ACEPTAR_CONCELLO:
                _aceptar_campo(campos["concello"], mejor)
                concello_aceptado = mejor
                scores_aceptados.append(mejor["score"])
                matching["concello"] = {"codigo": mejor["codigo"], "nome": mejor["nome"]}
                matching["provincia"] = _nombre_provincia(mejor["codigo"])
                if "provincia" in campos and campos["provincia"].get("value"):
                    prov = matching["provincia"]
                    if prov:
                        campos["provincia"]["value"] = prov["nome"]
                        campos["provincia"]["codigo_ine"] = prov["codigo"]
                        campos["provincia"]["match_score"] = mejor["score"]
    valor_localidade = _valor_campo(campos, "localidade")
    codigo_concello = concello_aceptado["codigo"] if concello_aceptado else None
    localidad_aceptada = None
    if valor_localidade and codigo_concello:
        candidatos_localidade = buscar_en_catalogo(catalogo, valor_localidade, "localidade", codigo_concello)
        if candidatos_localidade:
            mejor = candidatos_localidade[0]
            if _cumple_prefijo(mejor["codigo"], codigo_concello) and mejor["score"] >= UMBRAL_ACEPTAR_LOCALIDADE:
                _aceptar_campo(campos["localidade"], mejor)
                localidad_aceptada = mejor
                scores_aceptados.append(mejor["score"])
                matching["localidade"] = {"codigo": mejor["codigo"], "nome": mejor["nome"]}
    if codigo_concello and not localidad_aceptada and not valor_localidade:
        valor_parroquia = _valor_campo(campos, "parroquia")
        if valor_parroquia:
            candidatos_localidade = buscar_en_catalogo(catalogo, valor_parroquia, "localidade", codigo_concello)
            if candidatos_localidade:
                mejor = candidatos_localidade[0]
                if _cumple_prefijo(mejor["codigo"], codigo_concello) and mejor["score"] >= UMBRAL_ACEPTAR_LOCALIDADE:
                    campos["localidade"] = {"value": mejor["nome"], "confidence": mejor["score"], "bbox": [], "raw_text": valor_parroquia, "status": "review", "codigo_ine": mejor["codigo"], "match_score": mejor["score"], "inferido": True}
                    localidad_aceptada = mejor
                    scores_aceptados.append(mejor["score"])
                    matching["localidade"] = {"codigo": mejor["codigo"], "nome": mejor["nome"]}
        if not localidad_aceptada:
            valor_lugar = _valor_campo(campos, "lugar")
            if valor_lugar:
                inferida = _inferir_localidade_por_lugar(catalogo, codigo_concello, valor_lugar)
                if inferida:
                    campos["localidade"] = {"value": inferida["nome"], "confidence": inferida["score"], "bbox": [], "raw_text": valor_lugar, "status": "review", "codigo_ine": inferida["codigo"], "match_score": inferida["score"], "inferido": True}
                    localidad_aceptada = inferida
                    scores_aceptados.append(inferida["score"])
                    matching["localidade"] = {"codigo": inferida["codigo"], "nome": inferida["nome"]}
    valor_lugar = _valor_campo(campos, "lugar")
    codigo_localidade = localidad_aceptada["codigo"] if localidad_aceptada else (campos.get("localidade") or {}).get("codigo_ine")
    if valor_lugar and codigo_localidade:
        candidatos_lugar = [c for c in buscar_en_catalogo(catalogo, valor_lugar, "lugar", codigo_localidade) if _cumple_prefijo(c["codigo"], codigo_localidade)]
        if candidatos_lugar:
            matching["candidates"] = candidatos_lugar
            mejor = candidatos_lugar[0]
            if mejor["score"] >= UMBRAL_ACEPTAR_LUGAR:
                _aceptar_campo(campos["lugar"], mejor)
                scores_aceptados.append(mejor["score"])
                matching["lugar"] = {"codigo": mejor["codigo"], "nome": mejor["nome"]}
    if scores_aceptados:
        matching["match_confidence"] = round(min(scores_aceptados), 4)
    return matching


def _valor_campo(campos, nombre):
    if nombre in campos and campos[nombre].get("value"):
        return campos[nombre]["value"]
    return None


def _aceptar_campo(campo_datos, candidato):
    campo_datos["value"] = candidato["nome"]
    campo_datos["codigo_ine"] = candidato["codigo"]
    campo_datos["match_score"] = candidato["score"]


def _cumple_prefijo(codigo_hijo, codigo_padre):
    return codigo_hijo.startswith(codigo_padre)


def _inferir_localidade_por_lugar(catalogo, codigo_concello, texto_lugar):
    texto_norm = normalizar_para_catalogo(texto_lugar)
    por_localidade = {}
    for codigo_loc, nombre_loc, nombre_lugar, codigo_lugar in _lugares_por_concello(catalogo, codigo_concello):
        score = similitud(texto_norm, normalizar_para_catalogo(nombre_lugar))
        if score >= 0.80:
            prev = por_localidade.get(codigo_loc)
            if prev is None or score > prev[0]:
                por_localidade[codigo_loc] = (score, nombre_loc, nombre_lugar, codigo_lugar)
    if not por_localidade:
        return None
    mejor_codigo = max(por_localidade, key=lambda c: por_localidade[c][0])
    score, nombre_loc, nombre_lugar, codigo_lugar = por_localidade[mejor_codigo]
    segundos = [s for s in por_localidade.values() if s[0] == score]
    if len(segundos) > 1:
        return None
    return {"codigo": mejor_codigo, "nome": nombre_loc, "score": round(score, 4)}


def _lugares_por_concello(catalogo, codigo_concello):
    resultado = []
    for concellos in catalogo.values():
        for datos in concellos.values():
            if datos["codigo"] != codigo_concello:
                continue
            for nombre_loc, datos_loc in datos["localidades"].items():
                for lugar in datos_loc["lugares"]:
                    resultado.append((datos_loc["codigo"], nombre_loc, lugar["nome"], lugar["codigo"]))
            return resultado
    return resultado


def _candidatos(items, texto_ocr, umbral, maximo=None):
    texto_norm = normalizar_para_catalogo(texto_ocr)
    resultado = []
    for nombre, codigo in items:
        score = similitud(texto_norm, normalizar_para_catalogo(nombre))
        if score >= umbral:
            resultado.append({"codigo": codigo, "nome": nombre, "score": round(score, 4)})
    resultado.sort(key=lambda c: (-c["score"], c["nome"]))
    if maximo is not None:
        resultado = resultado[:maximo]
    return resultado


def buscar_en_catalogo(catalogo, texto_ocr, nivel, codigo_padre=None):
    if nivel == "concello":
        return _candidatos(_items_concellos(catalogo), texto_ocr, 0.70, 5)
    if nivel == "localidade":
        return _candidatos(_items_localidades(catalogo, codigo_padre), texto_ocr, 0.75, 5)
    if nivel == "lugar":
        return _candidatos(_items_lugares(catalogo, codigo_padre), texto_ocr, 0.80)
    if nivel == "provincia":
        return []
    return []


def centro_bbox(bbox):
    """Centro (x, y) de un bbox de 4 puntos [[x,y],...]."""
    if not bbox or len(bbox) != 4:
        return (0, 0)
    xs = [p[0] for p in bbox]
    ys = [p[1] for p in bbox]
    return (sum(xs) / 4, sum(ys) / 4)


def distancia(a, b):
    """Distancia euclidiana entre dos puntos (x, y)."""
    return math.hypot(a[0] - b[0], a[1] - b[1])


# ---------------------------------------------------------------------------
# Etiquetas conocidas -> campo del contrato
# ---------------------------------------------------------------------------
# Incluye variantes en gallego y castellano.
ETIQUETAS = [
    # (etiqueta_normalizada, campo_json, num_apariciones)
    # --- Nome ---
    ("nome", "nome", 1),
    ("nombre", "nome", 1),
    # --- Apelidos (solicitante e representante) ---
    ("primeiro apelido", "primeiroApelido", 2),
    ("primer apellido", "primeiroApelido", 2),
    ("segundo apelido", "segundoApelido", 2),
    ("segundo apellido", "segundoApelido", 2),
    # --- DNI ---
    ("nif pasaporte", "dni", 1),
    ("nif", "dni", 1),
    ("dni", "dni", 1),
    # --- Enderezo (solicitante e notificación) ---
    ("tipo de via", "tipoVia", 2),
    ("nome da via", "nomeVia", 2),
    ("nombre de la via", "nomeVia", 2),
    ("numero", "numero", 2),
    ("bloque", "bloque", 2),
    ("andar", "andar", 2),
    ("piso", "andar", 2),
    ("porta", "porta", 2),
    ("puerta", "porta", 2),
    ("parroquia", "parroquia", 2),
    ("lugar", "lugar", 2),
    ("cp", "cp", 2),
    ("codigo postal", "cp", 2),
    ("provincia", "provincia", 2),
    ("concello", "concello", 2),
    ("ayuntamiento", "concello", 2),
    ("localidade", "localidade", 2),
    ("localidad", "localidade", 2),
    # --- Contacto ---
    ("telefono", "telefono", 1),
    ("telefono mobil", "telefonoMovil", 2),
    ("telefono movil", "telefonoMovil", 2),
    ("correo electronico", "correo", 2),
    # --- Datos personais ---
    ("data de nacemento", "dataNacemento", 1),
    ("fecha de nacimiento", "dataNacemento", 1),
    ("sexo", "sexo", 1),
    ("xenero", "sexo", 1),
    ("genero", "sexo", 1),
    ("feminino", None, 0),
    ("femenino", None, 0),
    ("masculino", None, 0),
    # --- Representante ---
    ("nome razon social", "nomeRepresentante", 1),
    ("nombre razon social", "nomeRepresentante", 1),
    # --- Datos específicos do procedemento ---
    ("nome do titulo e ou estudos no sistema educativo estranxeiro", "tituloEstranxeiro", 1),
    ("nombre del titulo y o estudios en el sistema educativo extranjero", "tituloEstranxeiro", 1),
    ("pais", "paisTitulo", 2),
    ("nome do centro", "nomeCentro", 1),
    ("nombre del centro", "nomeCentro", 1),
    ("ano academico", "anoAcademico", 1),
    ("exames oficiais superados", "examesOficiais", 1),
    ("examenes oficiales superados", "examesOficiais", 1),
]

# Lista exhaustiva de etiquetas del formulario (para descartar candidatos).
ETIQUETAS_FORMULARIO = {
    # Del PDF limpio (etiquetas mecanografiadas)
    "nome", "nombre", "primeiro apelido", "primer apellido",
    "segundo apelido", "segundo apellido", "nif pasaporte", "nif",
    "dni", "tipo de via", "nome da via", "nombre de la via",
    "numero", "bloque", "andar", "piso", "porta", "puerta",
    "parroquia", "lugar", "cp", "codigo postal", "provincia",
    "concello", "ayuntamiento", "localidade", "localidad",
    "telefono", "telefono mobil", "telefono movil",
    "correo electronico", "data de nacemento", "fecha de nacimiento",
    "sexo", "xenero", "genero", "feminino", "femenino", "masculino",
    "nome razon social", "nombre razon social",
    "nome do titulo e ou estudos no sistema educativo estranxeiro",
    "nombre del titulo y o estudios en el sistema educativo extranjero",
    "pais", "nome do centro", "nombre del centro",
    "ano academico", "exames oficiais superados", "examenes oficiales superados",
    # Otras etiquetas que aparecen en el formulario
    "notifiquese a", "persona solicitante", "persona o entidad representante",
    "eleccion del medio de notificacion preferente", "electronica", "postal",
    "datos especificos del procedimiento",
    "nivel de las ensenanzas que solicita en el sistema educativo espanol",
    "nombre del titulo y o estudios en el sistema educativo espanol",
    "documentacion que se presenta", "con caracter general para todas las ensenanzas",
    "ensenanzas de formacion profesional o de regimen especial",
    "master en ensenanzas artisticas", "outra documentacion",
    "comprobacion de datos", "dninie da persoa solicitante",
    "dninie da persoa representante", "oponome a consulta",
    # Fragmentos
    "nie", "cif", "apellido", "domicilio", "movil", "correo", "email",
    "fecha", "nacimiento", "municipio", "calle",
}

# Mapeo campo -> id del formulario (para la extensión)
CAMPO_A_ID = {
    "nome": "nome",
    "primeiroApelido": "primeiroApelido",
    "segundoApelido": "segundoApelido",
    "dni": "doiSolicitante",
    "tipoVia": "enderezoSolicitanteTipoVia",
    "nomeVia": "enderezoSolicitanteNomeVia",
    "numero": "enderezoSolicitanteNumero",
    "bloque": "enderezoSolicitanteBloque",
    "andar": "enderezoSolicitanteAndar",
    "porta": "enderezoSolicitantePorta",
    "parroquia": "enderezoSolicitanteParroquia",
    "lugar": "enderezoSolicitanteCodLugar",
    "cp": "enderezoSolicitanteCp",
    "provincia": "enderezoSolicitanteCodProvincia",
    "concello": "enderezoSolicitanteCodConcello",
    "localidade": "enderezoSolicitanteCodLocalidade",
    "telefono": "telefono",
    "telefonoMovil": "mobil",
    "correo": "mail",
    "dataNacemento": "formularioHomologacion_solicitude_dataNacementoSolicitante",
    "sexo": "formularioHomologacion_solicitude_xeneroSolicitanteF",
    "nomeRepresentante": "nomeRepresentante",
    "tituloEstranxeiro": "nomeTituloExtranxeiro",
    "paisTitulo": "codPais",
    "nomeCentro": "nomeCentro",
    "anoAcademico": "codAnoAcademico",
    "examesOficiais": "examesOficiaisSuperados",
}


# ---------------------------------------------------------------------------
# Extracción PDF -> imagen
# ---------------------------------------------------------------------------

def extraer_primera_pagina_como_imagen(pdf_path: Path, salida_dir: Path, dpi: int = 300) -> Path:
    if not pdf_path.is_file():
        raise FileNotFoundError(f"No existe el PDF: {pdf_path}")

    salida_dir.mkdir(parents=True, exist_ok=True)
    salida_img = salida_dir / f"{pdf_path.stem}_p1.png"

    pdf = pdfium.PdfDocument(str(pdf_path))
    try:
        if len(pdf) < 1:
            raise ValueError(f"El PDF no tiene páginas: {pdf_path}")
        page = pdf[0]
        scale = dpi / 72.0
        bitmap = page.render(scale=scale)
        pil_image = bitmap.to_pil()
        pil_image.save(str(salida_img), format="PNG")
    finally:
        pdf.close()

    return salida_img


# ---------------------------------------------------------------------------
# OCR con PaddleOCR-json
# ---------------------------------------------------------------------------

def ejecutar_paddleocr_json(imagen_path: Path) -> list:
    if not _PADDLE_OCR_JSON.is_file():
        raise FileNotFoundError(f"No existe PaddleOCR-json: {_PADDLE_OCR_JSON}")

    resultado = subprocess.run(
        [str(_PADDLE_OCR_JSON), f'-image_path={imagen_path}'],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=str(_PADDLE_OCR_JSON.parent),
        timeout=300,
    )

    if resultado.returncode != 0:
        raise RuntimeError(
            f"PaddleOCR-json falló (código {resultado.returncode}): "
            f"{resultado.stderr.strip()}"
        )

    salida = resultado.stdout.strip()
    if not salida:
        return []

    try:
        datos = json.loads(salida)
    except json.JSONDecodeError:
        inicio = salida.find("{")
        fin = salida.rfind("}")
        if inicio != -1 and fin != -1 and fin > inicio:
            datos = json.loads(salida[inicio : fin + 1])
        else:
            raise

    if isinstance(datos, dict):
        if datos.get("code") != 100:
            raise RuntimeError(
                f"PaddleOCR-json devolvió código {datos.get('code')}: "
                f"{datos.get('msg', 'sin mensaje')}"
            )
        datos = datos.get("data", [])
    elif not isinstance(datos, list):
        datos = []

    detecciones = []
    for item in datos:
        if not isinstance(item, dict):
            continue
        texto = item.get("text", "")
        box = item.get("box", [])
        score = item.get("score", 0.0)
        detecciones.append({
            "raw_text": texto,
            "bbox": box if isinstance(box, list) else [],
            "confidence": float(score) if score else 0.0,
        })
    return detecciones


# ---------------------------------------------------------------------------
# Validación de formato por campo
# ---------------------------------------------------------------------------

def es_valor_valido(campo, valor):
    """Devuelve True si el valor tiene el formato esperado para el campo."""
    if not valor:
        return False
    valor = valor.strip()
    if campo == "nomeRepresentante" and len(valor) < 4:
        return False
    if campo == "cp":
        return bool(re.fullmatch(r"\d{5}", valor))
    if campo == "dni":
        return bool(re.fullmatch(r"\d{8}[A-Za-z]|[XYZxyz]\d{7}[A-Za-z]", valor))
    if campo == "correo":
        return "@" in valor
    if campo == "dataNacemento":
        return bool(re.fullmatch(r"\d{2}/\d{2}/\d{4}", valor))
    if campo in ("telefono", "telefonoMovil"):
        return bool(re.fullmatch(r"\d{9}", valor.replace(" ", "")))
    if campo in ("numero", "bloque", "andar", "porta"):
        return bool(re.fullmatch(r"\d{1,4}[A-Za-z]?", valor))
    if campo == "sexo":
        return valor in ("F", "M")
    if campo == "anoAcademico":
        return bool(re.fullmatch(r"\d{3,4}", valor))
    return True


# ---------------------------------------------------------------------------
# Matching por palabras clave
# ---------------------------------------------------------------------------

def asignar_etiquetas_a_campos(detecciones: list, catalogo: dict = None):
    """
    Asigna detecciones a campos según etiquetas conocidas y ejecuta el
    matching territorial si se pasa el catalogo.

    Estrategia (formulario ED434A: etiquetas arriba, valores abajo):
    - Filtrar por confianza >= 0.4.
    - Encontrar todas las etiquetas (Levenshtein >= 0.75).
    - Para cada etiqueta, buscar el valor DEBAJO (dy > 0).
    - El valor debe estar alineado en la misma columna (dx pequeño).
    - Validar el formato del valor según el campo.
    - Si no se encuentra o no es válido, dejar el campo como missing.
    - Despues, aplicar el matching territorial sobre concello/localidade/lugar.

    Devuelve (campos, matching).
    """
    validas = [d for d in detecciones if d["confidence"] >= 0.4]
    validas.sort(key=lambda d: (centro_bbox(d["bbox"])[1], centro_bbox(d["bbox"])[0]))

    usadas_etiqueta = set()
    usadas_valor = set()
    campos = {}

    def es_etiqueta(texto_norm):
        for etq, _, _ in ETIQUETAS:
            if similitud(etq, texto_norm) >= 0.75:
                return True
        if texto_norm in ETIQUETAS_FORMULARIO:
            return True
        FRAGMENTOS = {"nif", "nie", "dni", "cif", "cp", "email", "mail"}
        if len(texto_norm) <= 4 and texto_norm in FRAGMENTOS:
            return True
        return False

    # 1. Encontrar todas las etiquetas
    etiquetas_encontradas = []
    for idx, d in enumerate(validas):
        texto_norm = normalizar(d["raw_text"])
        mejor_etq = None
        mejor_score = 0.0
        for etq, campo, num_ap in ETIQUETAS:
            if campo is None:
                continue
            score = similitud(etq, texto_norm)
            if score > mejor_score and score >= 0.75:
                mejor_score = score
                mejor_etq = (etq, campo, num_ap)
        if mejor_etq is not None:
            etiquetas_encontradas.append((idx, d, mejor_etq, mejor_score))

    # 2. Procesar cada etiqueta
    for idx, d, (etq, campo, num_ap), score in etiquetas_encontradas:
        if idx in usadas_etiqueta:
            continue
        usadas_etiqueta.add(idx)

        # Calcular dimensiones de la etiqueta
        if len(d["bbox"]) == 4:
            xs = [p[0] for p in d["bbox"]]
            ys = [p[1] for p in d["bbox"]]
            ancho_e = max(xs) - min(xs)
            altura_e = max(ys) - min(ys)
        else:
            ancho_e = 100
            altura_e = 30

        x_e, y_e = centro_bbox(d["bbox"])

        mejor_valor = None
        mejor_dist = float("inf")
        mejor_idx_valor = None

        for j, v in enumerate(validas):
            if j == idx or j in usadas_valor or j in usadas_etiqueta:
                continue
            texto_v_norm = normalizar(v["raw_text"])
            if es_etiqueta(texto_v_norm):
                continue

            x_v, y_v = centro_bbox(v["bbox"])
            dy = y_v - y_e
            dx = abs(x_v - x_e)

            # El valor debe estar DEBAJO (dy > 0, hasta 3 veces la altura de la etiqueta)
            # Y alineado en la misma columna (dx menor que el ancho de la etiqueta)
            if 0 < dy < 3 * altura_e and dx < ancho_e * 0.8:
                dist = dy
                if dist < mejor_dist:
                    mejor_dist = dist
                    mejor_valor = v
                    mejor_idx_valor = j

        if mejor_valor is not None:
            valor = mejor_valor["raw_text"]
            if es_valor_valido(campo, valor):
                usadas_valor.add(mejor_idx_valor)
                clave = campo if campo not in campos else f"{campo}_2"
                campos[clave] = {
                    "value": valor or None,
                    "confidence": mejor_valor["confidence"],
                    "bbox": mejor_valor["bbox"],
                    "raw_text": valor,
                    "status": "review" if valor else "missing",
                }

    # Detectar sexo (FEMININO / MASCULINO)
    for d in validas:
        texto_norm = normalizar(d["raw_text"])
        if "feminino" in texto_norm or "femenino" in texto_norm:
            campos["sexo"] = {
                "value": "F",
                "confidence": d["confidence"],
                "bbox": d["bbox"],
                "raw_text": d["raw_text"],
                "status": "review",
            }
            break
        elif "masculino" in texto_norm:
            campos["sexo"] = {
                "value": "M",
                "confidence": d["confidence"],
                "bbox": d["bbox"],
                "raw_text": d["raw_text"],
                "status": "review",
            }
            break

    # Matching territorial (despues del matching por palabras clave)
    matching = aplicar_matching_territorial(campos, catalogo) if catalogo else {}
    return campos, matching


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(argv):
    if len(argv) not in (2, 3):
        print("Uso: python scripts/ocr.py <ruta_al_pdf> [dpi]", file=sys.stderr)
        return 1

    pdf_path = Path(argv[1]).resolve()
    dpi = int(argv[2]) if len(argv) == 3 else 300
    salida_dir = _HERE.parent / "recursos" / "salida"

    try:
        img_path = extraer_primera_pagina_como_imagen(pdf_path, salida_dir, dpi)
        detecciones = ejecutar_paddleocr_json(img_path)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2

    # Matching territorial (carga el catalogo una vez con UTF-8 explicito)
    catalogo = cargar_catalogo()
    fields, matching = asignar_etiquetas_a_campos(detecciones, catalogo)

    # Añadir el id del formulario a cada campo
    for campo, datos in fields.items():
        if campo in CAMPO_A_ID:
            datos["form_id"] = CAMPO_A_ID[campo]

    # UTF-8 explicito en stdout: la redireccion > fichero del .bat no transcodifica
    # (en Windows consola usa cp1252; forzamos UTF-8 sin BOM para el JSON de salida)
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    salida_json = {
        "version": "1.0",
        "source_pdf": pdf_path.name,
        "pages": 1,
        "fields": fields,
        "matching": matching,
    }

    print(json.dumps(salida_json, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))