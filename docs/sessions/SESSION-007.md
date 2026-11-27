# SESSION-007 — Matching Territorial

## Fecha
2026-11-27

## Objetivo
Implementar el matching territorial en `scripts/ocr.py` usando el catálogo
territorial de Galicia y ejecutar el pipeline sobre los cinco PDFs de ejemplo
(3 manuscritos + 2 mecanografiados), generando un informe de análisis
antes/después.

## Ficheros generados (JSON de salida, UTF-8 sin BOM, tamaño > 0)

- `recursos/salida/manuscrito-001_matching.json`
- `recursos/salida/manuscrito-002_matching.json`
- `recursos/salida/manuscrito-003_matching.json`
- `recursos/salida/mecanografiado-001_matching.json`
- `recursos/salida/mecanografiado-002_matching.json`

## Resultados del matching territorial

| PDF | concello | localidade | lugar | match_confidence |
|-----|----------|------------|-------|------------------|
| manuscrito-001 | Ourense (32054) corregido desde "ourense" | Ourense (3205400) corregido desde "oorense" | null | 0.8571 |
| manuscrito-002 | sin cambios (sin concello detectado) | sin cambios | - | 0.0 |
| manuscrito-003 | sin cambios ("Oercnsc" < 0.70) | sin cambios | - | 0.0 |
| mecanografiado-001 | sin cambios (mejor candidato ≈ 0.818 < 0.85) | sin cambios | - | 0.0 |
| mecanografiado-002 | Monterrei (32050) | San cristovo (San Cristovo) (3205009) | San Cristovo (320500901) | 1.0 |

- manuscritoi-001: provincia "3204" corregida a "Ourense" (32) derivada del concello.
- mecanografiado-002: prefijos INE validados (3205009 empieza por 32050; 320500901 empieza por 3205009).
- Ningún campo empeoró; todos los valores siguen con `status: "review"`.

## Informe de análisis
`docs/validation/MATCHING_TERRITORIAL_ANALYSIS.md`.

## Ficheros modificados

- `scripts/ocr.py`: añadidas `cargar_catalogo`, `normalizar_para_catalogo`,
  `buscar_en_catalogo` y `aplicar_matching_territorial` (integrada al final de
  `asignar_etiquetas_a_campos`); `main()` carga el catálogo una vez y escribe
  `matching` en la salida; `sys.stdout.reconfigure(encoding="utf-8")` para
  salida UTF-8 sin BOM mediante redirección `>` del `.bat`.

## Ficheros de documentación actualizados

- `docs/HANDOVER.md`: reflejado nuevo estado (matching territorial implementado).
- `docs/PROJECT_STATUS.md`: matching territorial marcado como completado.
- `docs/NEXT_SESSION.md`: tareas actualizadas (matching territorial completado;
  siguiente: extensión Chrome, baseline, codAnoAcademico).
- `docs/CHANGELOG.md`: entrada 2026-11-27 añadida.

## Verificación final

- `scripts/ocr.py` incluye las nuevas funciones (`cargar_catalogo`,
  `buscar_en_catalogo`, `aplicar_matching_territorial`, etc.).
- Los cinco JSONs se generaron correctamente (tamaño > 0, JSON válido).
- Los ficheros de documentación existen y son válidos.
- Ninguna otra parte del código fue modificada (solo `scripts/ocr.py` y
  ficheros de documentación).