# Informe de Análisis — Matching Territorial (Sesión 007)

## Resumen

Se implementó el matching territorial en `scripts/ocr.py` sobre el catálogo
`recursos\catalogo-hovaes-lugares-galicia-completo.json` (317 concellos,
3.790 localidades, 34.164 lugares) y se ejecutó el pipeline sobre los cinco
PDFs de ejemplo (3 manuscritos + 2 mecanografiados). Todo el procesamiento es
local y los JSONs de salida se escriben en UTF-8 sin BOM.

## Metodología aplicada

- `cargar_catalogo()`: lectura del catálogo con UTF-8 explícito (sin BOM), con
  caché en memoria para no volver a leerlo en cada ejecución.
- `normalizar_para_catalogo()`: misma normalización que el matching por palabras
  clave (minúsculas, sin tildes, espacios colapsados).
- `buscar_en_catalogo(texto_ocr, nivel, codigo_padre)`: Levenshtein normalizado.
  - `concello`: umbral ≥ 0.70, hasta 5 candidatos entre los 317 concellos.
  - `localidade`: umbral ≥ 0.75 dentro del concello elegido, hasta 5 candidatos.
  - `lugar`: umbral ≥ 0.80 dentro de la localidad elegida, todos los candidatos
    que superen el umbral.
  - `provincia`: no se busca, se deriva de los dos primeros dígitos del concello.
- Corrección automática solo si hay candidato claro (score ≥ 0.85).
- Inferencia de `localidade` cuando `concello` está detectado pero `localidade`
  no, a partir del campo `parroquia` o del campo `lugar`.
- Validación de coherencia por prefijo INE en cada nivel:
  `localidade.codigo` empieza por `concello.codigo`;
  `lugar.codigo` empieza por `localidade.codigo`.
- `matching` al contrato de `DATA_MODEL.md` (provincia, concello, localidad,
  lugar, match_confidence, candidates). Los campos territoriales de `fields`
  llevan además `codigo_ine` y `match_score`. Todos los valores siguen con
  `status: "review"` (requieren revisión del usuario).
- `main()` carga el catálogo una vez y escribe `matching` en la salida JSON;
  `sys.stdout.reconfigure(encoding="utf-8")` para que la redirección `>` del
  `.bat` produzca UTF-8 sin BOM (la consola de Windows usa cp1252).

## Resultado por PDF

### manuscrito-001 (manuscrito)

Antes: provincia="3204" (incoherente), concello="ourense", localidade="oorense",
lugar=ausente, matching={}.

Después: provincia="Ourense" (32), concello="Ourense" (32054),
localidade="Ourense" (3205400), lugar=null.

- `concello`: corregido "ourense" → "Ourense" (score 1.0).
- `localidade`: corregido "oorense" → "Ourense" (score 0.8571, ≥ 0.85).
- `provincia`: corregido de "3204" a "Ourense" (derivada del concello aceptado;
  antes era un valor incoherente, parecía un CP).
- Campos rellenados que faltaban: ninguno nuevo (los campos ya existían; ahora
  llevan `codigo_ine` y `match_score`).
- ¿Empeoró algún campo?: no.
- `matching`: {provincia: {32, Ourense}, concello: {32054, Ourense},
  localidade: {3205400, Ourense}, lugar: null, match_confidence: 0.8571,
  candidates: []}.

### manuscrito-002 (manuscrito)

Antes: provincia="Oonnse", sin concello/localidade/lugar, matching={}.

Después: igual. No hay concello detectado, por lo que no hay nivel superior
del cual derivar la provincia ni dentro del cual buscar la localidad; no se
modifica nada.

- ¿Empeoró algún campo?: no.

### manuscrito-003 (manuscrito)

Antes: provincia="Mureosc", concello="Oercnsc", localidade="Ourensc",
matching={}.

Después: igual. "Oercnsc" no alcanza el umbral mínimo de concello (≥ 0.70; el
mejor candidato "Ourense" está alrededor de 0.57), por lo que no se corrige ni
se avanza a localidad/lugar. No se introduce ruido.

- ¿Empeoró algún campo?: no.

### mecanografiado-001 (mecanografiado)

Antes: provincia="OURENSE", concello="CARBALLINO,", localidade="OCARBALLINOM",
lugar=ausente, matching={}.

Después: igual. El mejor candidato de concello para "CARBALLINO," es
"O Carballiño" con score ≈ 0.818 < 0.85 (umbral de corrección); no se considera
candidato claro y no se corrige automáticamente. Sin concello aceptado, no se
busca la localidad.

- ¿Empeoró algún campo?: no. El valor OCR se conserva para revisión del usuario.

### mecanografiado-002 (mecanografiado)

Antes: provincia="OURENSE", concello="Monterrei",
localidade="San cristovo (San Cristovo)", lugar="San Cristovo", matching={}.

Después: provincia="Ourense" (32), concello="Monterrei" (32050),
localidade="San cristovo (San Cristovo)" (3205009),
lugar="San Cristovo" (320500901).

- `concello`: mantenido "Monterrei", ahora con `codigo_ine` 32050 (score 1.0).
- `localidade`: mantenido, ahora con `codigo_ine` 3205009 (score 1.0).
- `lugar`: mantenido "San Cristovo", ahora con `codigo_ine` 320500901
  (score 1.0).
- `provincia`: "OURENSE" → "Ourense" (32), derivada del concello.
- Validación prefijo INE: 3205009 empieza por 32050; 320500901 empieza por
  3205009. OK.
- `matching`: confianza 1.0, candidates=[{San Cristovo, 320500901, 1.0}].

## Comparación antes/después (resumen)

| PDF | concello antes → después | localidade antes → después | lugar antes → después | matching relleno |
|-----|--------------------------|----------------------------|-----------------------|------------------|
| manuscrito-001 | ourense → Ourense (32054) | oorense → Ourense (3205400) | - → null | provincia + concello + localidade (confianza 0.8571) |
| manuscrito-002 | - → - | - → - | - → - | (sin cambios) |
| manuscrito-003 | Oercnsc → Oercnsc | Ourensc → Ourensc | - → - | (sin cambios) |
| mecanografiado-001 | CARBALLINO, → CARBALLINO, | OCARBALLINOM → OCARBALLINOM | - → - | (sin cambios; mejor candidato ≈ 0.818 < 0.85) |
| mecanografiado-002 | Monterrei → Monterrei (32050) | San cristovo (San Cristovo) → igual (3205009) | San Cristovo → San Cristovo (320500901) | completa, confianza 1.0 |

## Conclusión

- El matching territorial corrige valores de `concello`/`localidade` cuando el
  OCR se acerca lo suficiente (manuscrito-001: "ourense"/"oorense" → "Ourense")
  y completa códigos INE cuando los valores OCR son correctos (mecanografiado-002:
  coincidencia exacta, confianza 1.0).
- Con manuscritos de baja calidad (manuscrito-003: "Oercnsc") el OCR se desvía
  demasiado y no alcanza los umbrales; no se introduce ruido (los valores
  incorrectos se conservan tal cual para revisión del usuario, sin forzar
  correcciones erróneas).
- En mecanografiado-001 el mejor candidato de concello queda por debajo del
  umbral de corrección (0.818 < 0.85), por lo que no se corrige automáticamente;
  el valor se conserva para revisión del usuario.
- Ningún campo empeoró; todo valor sigue con `status: "review"` y requiere
  revisión del usuario, conforme al contrato de `DATA_MODEL.md`.
- La provincia se deriva correctamente del concello aceptado (prefijo INE de 2
  dígitos) y la coherencia de prefijos (concello/localidad/lugar) se valida en
  cada nivel.

## Verificación

- `scripts/ocr.py` incluye `cargar_catalogo`, `normalizar_para_catalogo`,
  `buscar_en_catalogo` y `aplicar_matching_territorial`.
- Los cinco JSONs se generaron correctamente (tamaño > 0, JSON válido, UTF-8
  sin BOM):
  - `recursos/salida/manuscrito-001_matching.json` (8401 bytes)
  - `recursos/salida/manuscrito-002_matching.json` (4258 bytes)
  - `recursos/salida/manuscrito-003_matching.json` (9220 bytes)
  - `recursos/salida/mecanografiado-001_matching.json` (8812 bytes)
  - `recursos/salida/mecanografiado-002_matching.json` (10417 bytes)