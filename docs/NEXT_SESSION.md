# NEXT SESSION

## Objetivo

Cerrar la fase de definición de arquitectura y empezar la implementación del pipeline OCR y de la extensión Chrome.

## Tareas

- [ ] Actualizar `PROJECT_STATUS.md`, `HANDOVER.md`, `CHANGELOG.md` y escribir `SESSION-002.md` (cierre de esta sesión).
- [ ] Implementar el esqueleto del pipeline OCR:
  - `scripts/ocr.py`: recibe una ruta de PDF, extrae la primera hoja, rasteriza con pypdfium2, llama a PaddleOCR-json, normaliza texto, hace el matching territorial y devuelve el JSON del contrato (`DATA_MODEL.md`).
  - `iniciar_ocr.bat`: lanza `python.exe scripts/ocr.py` y abre el socket HTTP local.
  - Fichero de estado en `%TEMP%\authovaes-ocr.json`.
- [ ] Implementar el esqueleto de la extensión Chrome:
  - `manifest.json` (MV3).
  - `background.js`: lee el fichero de estado, hace `fetch()` al puerto, recibe el JSON.
  - `content.js`: espera la carga dinámica de los selects, inyecta los valores por `id`, marca los campos como revisados.
- [ ] Baseline con PDFs reales (10 PDFs, marcar campos correctos/incorrectos por campo, ver `OCR_VALIDATION.md`).
- [ ] Decidir la licencia del proyecto (o confirmar que se mantiene sin licencia).
- [ ] (Opcional) Recibir el JSON del mapeo `codAnoAcademico` -> año y documentarlo en `FORM_ANALYSIS.md`.

## Resultado esperado

- Pipeline OCR mínimo funcionando con un PDF de prueba.
- Extensión Chrome mínima que precarga el JSON en el formulario.
- Baseline de OCR con 10 PDFs (aunque sea parcial).

## Riesgos a vigilar

- Precisión OCR en manuscrito (menos del 30% según estudio externo).
- Carga dinámica de los selects del formulario: la extensión debe esperar y disparar `change` en cascada.
- Duplicados: la UI debe presentarlos como filas separadas.