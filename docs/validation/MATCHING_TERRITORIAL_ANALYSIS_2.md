# Informe de Análisis — Umbral de Corrección Territorial 0.80 (Sesión 008)

## Resumen

Se bajó el umbral de corrección automática del matching territorial de **0.85 a 0.80** en
`scripts/ocr.py` (tres niveles: concello, localidade y lugar) y se volvió a ejecutar el
pipeline sobre los cinco PDFs de ejemplo (3 manuscritos + 2 mecanografiados). El objetivo
era recuperar el caso `mecanografiado-001`, cuyo concello "O Carballiño" tenía un score
de ~0.818 y se quedaba por debajo del umbral 0.85.

## Cambio aplicado

En `scripts/ocr.py`:

```python
UMBRAL_ACEPTAR_CONCELLO = 0.80
UMBRAL_ACEPTAR_LOCALIDADE = 0.80
UMBRAL_ACEPTAR_LUGAR = 0.80
```

Antes (sesión 007): todos en `0.85`. Todo lo demás del pipeline se mantiene igual
(`cargar_catalogo`, `normalizar_para_catalogo`, `buscar_en_catalogo`,
`aplicar_matching_territorial`, validación de prefijo INE, provincia derivada,
salida UTF-8 sin BOM).

## Resultado por PDF (umbral 0.80 vs 0.85)

### manuscrito-001 (manuscrito)

Sin cambios respecto a la sesión 007.
- provincia="Ourense" (32), concello="Ourense" (32054), localidade="Ourense" (3205400),
  lugar=null, match_confidence=0.8571.
- Los valores OCR "ourense"/"oorense" ya alcanzaban 1.0 / 0.8571, así que seguirán
  corrigiéndose con 0.80 (no hay diferencia visible).

### manuscrito-002 (manuscrito)

Sin cambios. No hay concello detectado (provincia="Oonnse"), por lo que no hay nivel
superior del cual derivar ni dentro del cual buscar. match_confidence=0.0.

### manuscrito-003 (manuscrito)

Sin cambios. "Oercnsc" no alcanza ni el umbral mínimo de búsqueda de concello (≥ 0.70;
el mejor candidato "Ourense" está alrededor de 0.57), por lo que no se corrige ni se
avanza a localidad/lugar. match_confidence=0.0.

### mecanografiado-001 (mecanografiado) — CASO CLAVE

**Antes (umbral 0.85)**: sin cambios. concello="CARBALLINO," sin corregir (mejor
candidato "O Carballiño" ≈ 0.818 < 0.85); localidade="OCARBALLINOM" sin corregir;
provincia="OURENSE" sin corregir; matching vacío.

**Después (umbral 0.80)**:
- concello: "CARBALLINO," → **"Carballiño (O)" (32019)**, score 0.8333 ≥ 0.80. ✅
- provincia: "OURENSE" → **"Ourense" (32)**, derivada del concello aceptado. ✅
- localidade: "OCARBALLINOM" se mantiene (no hay localidad dentro del concello
  Carballiño 32019 que alcance 0.80 ni cumpla prefijo; no se fuerza).
- lugar: ausente, null.
- matching: {provincia: {32, Ourense}, concello: {32019, Carballiño (O)},
  localidade: null, lugar: null, match_confidence: 0.8333, candidates: []}.

### mecanografiado-002 (mecanografiado)

Sin cambios. Coincidencia exacta en todos los niveles.
- provincia="Ourense" (32), concello="Monterrei" (32050),
  localidade="San cristovo (San Cristovo)" (3205009), lugar="San Cristovo" (320500901),
  match_confidence=1.0. Prefijos INE válidos.

## Comparación antes/después (resumen)

| PDF | concello 0.85 → 0.80 | localidade 0.85 → 0.80 | lugar 0.85 → 0.80 | conf 0.85 → 0.80 |
|-----|----------------------|------------------------|-------------------|------------------|
| manuscrito-001 | Ourense (32054) → igual | Ourense (3205400) → igual | null → igual | 0.8571 → igual |
| manuscrito-002 | - → - | - → - | - → - | 0.0 → igual |
| manuscrito-003 | - → - | - → - | - → - | 0.0 → igual |
| mecanografiado-001 | CARBALLINO, → **Carballiño (O) (32019)** | OCARBALLINOM → igual | - → null | 0.0 → 0.8333 |
| mecanografiado-002 | Monterrei (32050) → igual | San cristovo (3205009) → igual | San Cristovo (320500901) → igual | 1.0 → igual |

## Respuesta a las preguntas del informe

**¿Se ha corregido el concello de `mecanografiado-001` ("OCARBALLINOM" → "O Carballiño")?**

Sí. El valor OCR del campo concello era "CARBALLINO," y, con el umbral 0.80, el
mejor candidato "Carballiño (O)" (código INE 32019, provincia Ourense) alcanza un
score de 0.8333 ≥ 0.80, por lo que se corrige automáticamente. Además, la provincia
se deriva y corrige de "OURENSE" a "Ourense" (32). La localidad "OCARBALLINOM" no
se corrige porque dentro del concello Carballiño no hay una localidad que alcance
0.80; se deja para revisión del usuario.

**¿Ha empeorado algún campo? (falsos positivos, correcciones incorrectas)**

No. Ningún campo que estuviera correcto se ha estropeado:
- El concello corregido "Carballiño (O)" (32019) es un concello real de Ourense
  (código 32xxxx), coherente con el prefijo INE y con la provincia "OURENSE" leída
  por OCR. No es un falso positivo evidente.
- Los manuscritos de baja calidad (002, 003) siguen sin cambios (no se introduce
  ruido: valores incorrectos se conservan tal cual para revisión del usuario).
- mecánografiado-002 mantiene su coincidencia exacta (confianza 1.0).
- Todos los valores siguen con `status: "review"` (requieren revisión del usuario).

**¿Ha mejorado algún otro campo?**

Sí, en `mecanografiado-001`:
- `provincia`: de "OURENSE" (sin corregir, sin código INE) a "Ourense" (32), derivada
  del concello aceptado. Ahora lleva `codigo_ine` y `match_score`.
- `concello`: de "CARBALLINO," (sin corregir) a "Carballiño (O)" (32019), con código
  INE y score 0.8333.

## Conclusión

Bajar el umbral de 0.85 a 0.80 recupera el caso `mecanografiado-001`: el concello
"CARBALLINO," se corrige a "Carballiño (O)" (32019) y la provincia se deriva a
"Ourense" (32), sin introducir falsos positivos ni empeorar ningún otro campo. Los
PDFs cuyos valores OCR están muy desviados (manuscritos 002 y 003) siguen sin
corrección automática, lo que evita ruido. El cambio es seguro y recomendable.

## Verificación

- `scripts/ocr.py` tiene los tres umbrales en `0.80` (`UMBRAL_ACEPTAR_CONCELLO`,
  `UMBRAL_ACEPTAR_LOCALIDADE`, `UMBRAL_ACEPTAR_LUGAR`).
- Los cinco JSONs se generaron correctamente (tamaño > 0, JSON válido, UTF-8 sin BOM):
  - `recursos/salida/manuscrito-001_matching.json` (8401 bytes)
  - `recursos/salida/manuscrito-002_matching.json` (4258 bytes)
  - `recursos/salida/manuscrito-003_matching.json` (9220 bytes)
  - `recursos/salida/mecanografiado-001_matching.json` (9051 bytes)
  - `recursos/salida/mecanografiado-002_matching.json` (10417 bytes)