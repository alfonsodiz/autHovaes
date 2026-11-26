# SESSION-006 — Baseline de PDFs Manuscritos

## Fecha

2026-11-26

## Objetivo

Ejecutar el pipeline OCR sobre los tres PDFs manuscritos y analizar la coherencia de los valores extraídos, ya que no se dispone de los valores reales (protección de datos).

## Ficheros generados

- `recursos/salida/manuscrito-001_matching.json`
- `recursos/salida/manuscrito-002_matching.json`
- `recursos/salida/manuscrito-003_matching.json`
- `docs/validation/MATCHING_BASELINE_MANUSCRITOS.md` (informe de análisis)

## Resultados por PDF

| PDF | Campos rellenados | Coherentes | Incoherentes | Vacíos | Tasa coherencia |
|-----|------------------|------------|--------------|--------|-----------------|
| manuscritoi-001 | 18 | 9 | 9 | 11 | 50% |
| manuscritoi-002 | 9 | 5 | 4 | 16 | 56% |
| manuscritoi-003 | 20 | 9 | 11 | 9 | 45% |
| **Total** | **47** | **23** | **24** | **36** | **~49%** |

## Comparación con Mecanografiados

| Métrica | Mecanografiados (sesión 005) | Manuscritos (sesión 006) |
|---------|------------------------------|--------------------------|
| Coherencia global | ~84-92% | ~49% |
| Campos vacíos | Pocos | Muchos |
| Errores OCR en valores | Mínimos | Frecuentes |
| Campos críticos no detectados | Ninguno | `dni`, `cp`, `dataNacemento`, `telefono` |

## Campos que más fallan con manuscritos

1. **`nome` / `primeiroApelido` / `segundoApelido`**: fragmentos sueltos (`na`, `Pe`, `anos`).
2. **`provincia` / `concello` / `localidade`**: letras confusas (`Oercnsc`, `Mureosc`, `Oonnse`).
3. **`correo`**: dominio corrupto (`gma/.com`, `amail.Com`).
4. **`tipoVia` / `nomeVia`**: valores muy cortos o fragmentados (`R5a`, `PoSll`, `Veea`).
5. **`dni`, `cp`, `dataNacemento`, `telefono`**: no detectados en ninguno de los 3 PDFs.

## Conclusión

El matching por palabras clave funciona notablemente peor con manuscritos que con mecanografiados. La tasa de coherencia baja del ~84-92% al ~49%. Todo valor requiere revisión obligatoria del usuario.

## Ficheros modificados

- `docs/HANDOVER.md` — notas de sesión 006 añadidas
- `docs/PROJECT_STATUS.md` — baseline de manuscritos marcado como completado
- `docs/NEXT_SESSION.md` — tareas completadas y riesgos actualizados
- `docs/CHANGELOG.md` — entrada 2026-11-26 (sesión 006) añadida

## Ficheros creados

- `docs/validation/MATCHING_BASELINE_MANUSCRITOS.md` — informe de baseline
- `docs/sessions/SESSION-006.md` — este registro

## Verificación final

- `recursos/salida/manuscrito-001_matching.json`: generado, tamaño > 0, JSON válido ✅
- `recursos/salida/manuscrito-002_matching.json`: generado, tamaño > 0, JSON válido ✅
- `recursos/salida/manuscrito-003_matching.json`: generado, tamaño > 0, JSON válido ✅
- `scripts/ocr.py`: no modificado (según requisitos de la sesión) ✅