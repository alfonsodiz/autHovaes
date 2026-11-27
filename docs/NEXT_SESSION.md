# NEXT SESSION

## Objetivo

Continuar la implementación del pipeline OCR y de la extensión Chrome. La fase de definición de arquitectura está cerrada (ADR-001 y ADR-003 aceptadas).

## Tareas

- [ ] Integrar PaddleOCR-json en `scripts/ocr.py` (imagen → texto OCR).
  - Verificar que `paddleocr-json.exe` se ejecuta.
  - Entender el formato de entrada/salida.
  - Mapear la salida al contrato JSON (`DATA_MODEL.md`).
- [ ] Normalización de texto (minúsculas, sin tildes, espacios colapsados, sin paréntesis).
- [x] Matching territorial (Levenshtein + validación por prefijo INE), con umbrales 0.70/0.75/0.80 y N=5: implementado y ejecutado sobre los 5 PDFs de ejemplo.
- [ ] Escribir `iniciar_ocr.bat` definitivo (con socket HTTP local, fichero de estado en `%TEMP%`, token compartido).
- [ ] Extensión Chrome (`manifest.json`, `background.js`, `content.js`).
  - Lectura del fichero de estado en `%TEMP%`.
  - `fetch()` al puerto efímero.
  - Espera de carga dinámica de los selects.
  - Inyección por `id` y disparo de `change` en cascada.
- [ ] Baseline con PDFs reales (`OCR_VALIDATION.md`): 10 PDFs, marcar campos correctos/incorrectos por campo.
- [ ] (Opcional) Recibir el JSON del mapeo `codAnoAcademico` → año y documentarlo en `FORM_ANALYSIS.md`.

## Resultado esperado

- Pipeline OCR completo: PDF → imagen → OCR → normalización → matching → JSON.
- Extensión Chrome que precarga el JSON en el formulario ED434A.
- Baseline de OCR con 10 PDFs.

## Tareas completadas en esta sesión

- [x] Corregir problemas de asignación de campos en `scripts/ocr.py`:
    - [x] `parroquia` no debe aceptar provincias (`OURENSE`)
    - [x] `nome` no debe aceptar tipos de vía (`AVENIDA`)
    - [x] `lugar` no debe aceptar emails
- [x] Baseline de PDFs manuscritos (`manuscrito-001`, `manuscrito-002`, `manuscrito-003`):
    - [x] Ejecutar pipeline con los 3 PDFs manuscritos
    - [x] Analizar coherencia de campos (formato, etiquetas como valores, fragmentos)
    - [x] Generar informe `docs/validation/MATCHING_BASELINE_MANUSCRITOS.md`

## Riesgos a vigilar

- Precisión OCR en manuscrito (menos del 30% según estudio externo; tasa de coherencia ~49% medida en sesión 006).
- Campos críticos no detectados en manuscritos: `dni`, `cp`, `dataNacemento`, `telefono`.
- Carga dinámica de los selects del formulario: la extensión debe esperar y disparar `change` en cascada.
- Duplicados: la UI debe presentarlos como filas separadas con código INE visible.
- HTTP local: bind solo a `127.0.0.1`, CORS estricto, token compartido.