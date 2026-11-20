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
# Orden: las que aparecen primero en el PDF. Si hay duplicados (p. ej. "TIPO
# DE VÍA" dos veces), se asignan por orden de aparición.
# "consume_next" indica cuántas apariciones de la etiqueta hay en el PDF
# (1 = solo una; 2 = dos, la primera para solicitante, la segunda para
# notificación/representante).
ETIQUETAS = [
    # (etiqueta_normalizada, campo_json, num_apariciones)
    ("nome", "nome", 1),
    ("primeiro apelido", "primeiroApelido", 2),  # 1º solicitante, 2º representante
    ("segundo apelido", "segundoApelido", 2),    # 1º solicitante, 2º representante
    ("nif pasaporte", "dni", 1),
    ("tipo de via", "tipoVia", 2),               # 1º solicitante, 2º notificación
    ("nome da via", "nomeVia", 2),
    ("numero", "numero", 2),
    ("bloque", "bloque", 2),
    ("andar", "andar", 2),
    ("porta", "porta", 2),
    ("parroquia", "parroquia", 2),
    ("lugar", "lugar", 2),
    ("cp", "cp", 2),
    ("provincia", "provincia", 2),
    ("concello", "concello", 2),
    ("localidade", "localidade", 2),
    ("telefono", "telefono", 1),
    ("telefono mobil", "telefonoMovil", 2),      # 1º solicitante, 2º notificación
    ("correo electronico", "correo", 2),          # 1º solicitante, 2º notificación
    ("data de nacemento", "dataNacemento", 1),
    ("sexo", "sexo", 1),
    ("feminino", None, 0),                        # solo valor, no campo
    ("masculino", None, 0),
    ("nome razon social", "nomeRepresentante", 1),
    ("nome do titulo e ou estudos no sistema educativo estranxeiro", "tituloEstranxeiro", 1),
    ("pais", "paisTitulo", 2),                    # 1º país dirección, 2º país título
    ("nome do centro", "nomeCentro", 1),
    ("ano academico", "anoAcademico", 1),
    ("exames oficiais superados", "examesOficiais", 1),
]

# Lista exhaustiva de etiquetas del formulario (extraída del PDF limpio).
# Se usa en `es_etiqueta` para descartar candidatos que sean etiquetas.
ETIQUETAS_FORMULARIO = {
    # Del PDF limpio (etiquetas mecanografiadas)
    "nome",
    "primeiro apelido",
    "segundo apelido",
    "nif pasaporte",
    "tipo de via",
    "nome da via",
    "numero",
    "bloque",
    "andar",
    "porta",
    "parroquia",
    "lugar",
    "cp",
    "provincia",
    "concello",
    "localidade",
    "telefono",
    "telefono mobil",
    "correo electronico",
    "data de nacemento",
    "sexo",
    "feminino",
    "masculino",
    "nome razon social",
    "nome do titulo e ou estudos no sistema educativo estranxeiro",
    "pais",
    "nome do centro",
    "ano academico",
    "exames oficiais superados",
    # Otras etiquetas que aparecen en el formulario (no en ETIQUETAS)
    "ayuntamiento",
    "fecha de nacimiento",
    "nombre de la via",
    "nombre dela via",
    "piso",
    "puerta",
    "notifiquese a",
    "persona solicitante",
    "persona o entidad representante",
    "eleccion del medio de notificacion preferente",
    "electronica",
    "postal",
    "datos especificos del procedimiento",
    "nivel de las ensenanzas que solicita en el sistema educativo espanol",
    "nombre del titulo y o estudios en el sistema educativo espanol",
    "documentacion que se presenta",
    "con caracter general para todas las ensenanzas",
    "ensenanzas de formacion profesional o de regimen especial",
    "master en ensenanzas artisticas",
    "outra documentacion",
    "comprobacion de datos",
    "dninie da persoa solicitante",
    "dninie da persoa representante",
    "oponome a consulta",
    # Fragmentos que el OCR detecta como etiquetas
    "nif",
    "nie",
    "dni",
    "cif",
    "nombre",
    "apellido",
    "domicilio",
    "telefono",
    "movil",
    "correo",
    "email",
    "fecha",
    "nacimiento",
    "provincia",
    "municipio",
    "localidad",
    "calle",
    "numero",
    "piso",
    "puerta",
    "codigo postal",
    "cp",
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
    valor = valor.strip()  # quitar espacios
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

def asignar_etiquetas_a_campos(detecciones: list) -> dict:
    """
    Asigna detecciones a campos según etiquetas conocidas.
    
    Estrategia diseñada para el formulario ED434A (etiquetas arriba, valores abajo):
    - Filtrar por confianza >= 0.4.
    - Encontrar todas las etiquetas (Levenshtein >= 0.75).
    - Para cada etiqueta, buscar el valor DEBAJO (dy > 0).
    - El valor debe estar alineado en la misma columna (dx pequeño).
    - Validar el formato del valor según el campo.
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

            # El valor debe estar DEBAJO (dy > 0, hasta 4 veces la altura de la etiqueta)
            # Y alineado en la misma columna (dx menor que el ancho de la etiqueta)
            if 0 < dy < 4 * altura_e and dx < ancho_e * 0.8:
                # Preferimos el valor más cercano verticalmente
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

    return campos

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

    # Matching
    fields = asignar_etiquetas_a_campos(detecciones)

    # Añadir el id del formulario a cada campo
    for campo, datos in fields.items():
        if campo in CAMPO_A_ID:
            datos["form_id"] = CAMPO_A_ID[campo]

    salida_json = {
        "version": "1.0",
        "source_pdf": pdf_path.name,
        "pages": 1,
        "fields": fields,
        "matching": {},
    }

    print(json.dumps(salida_json, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))