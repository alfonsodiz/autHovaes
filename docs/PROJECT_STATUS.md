# PROJECT STATUS

## Fase actual

**Implementación** (no «Definición de arquitectura»). La fase de arquitectura está cerrada con las ADR-001 y ADR-003 aceptadas y documentadas. El pipeline OCR mínimo (PDF → imagen) está funcionando en modo de prueba.

- Fase: **Implementación**
- Documentación: castellano (sin cambiar la política de traducción)
- Repositorio: `https://github.com/alfonsodiz/autHovaes` (privado)

## Completado

- [x] Estructura documental
- [x] Catálogo territorial cargado y analizado (317 concellos, 3.790 localidades, 34.164 lugares)
- [x] Decisión de matching por niveles (ADR-002)
- [x] Contrato JSON de salida definido (`DATA_MODEL.md`)
- [x] Comportamiento del formulario ED434A observado y selectores documentados (`FORM_ANALYSIS.md`)
- [x] Traducción al castellano de los 21 ficheros `.md`
- [x] Corrección de mojibake en `CATALOGS.md`, `DATA_MODEL.md`, `DEVELOPMENT_ENVIRONMENT.md`
- [x] `GLOSARIO.md` creado
- [x] ADR-001: runtime OCR (PaddleOCR-json + HTTP local + `.bat` manual + fichero de estado `%TEMP%`)
- [x] ADR-003: extracción PDF → imagen (`pypdfium2`)
- [x] `OCR_PIPELINE.md` completado (umbrales, N, duplicados)
- [x] `DEPLOYMENT_CONSTRAINTS.md` actualizado (Native Messaging descartado, HTTP local documentado, bundle permitido)
- [x] Implementación del pipeline OCR mínimo
  - `scripts/ocr.py`: PDF → imagen PNG (pypdfium2, 300 DPI configurable)
  - `iniciar_ocr.bat`: lanza `python.exe scripts/ocr.py`
  - `scripts/__init__.py`: paquete de `scripts/`
- [x] Matching por palabras clave con variantes en castellano (nombre, apellido, tipo de vía, fecha de nacimiento, etc.)
- [x] Corrección de 5 falsos positivos en matching por palabras clave (`MATCHING_ANALYSIS_2.md`)
  - Tolerancia vertical reducida de `6 * altura_e` a `3 * altura_e`
  - `es_valor_valido` descarta `nomeRepresentante` < 4 caracteres
- [x] Baseline con PDFs mecanografiados (`MATCHING_BASELINE_MECANOGRAFADOS.md`, `MATCHING_ANALYSIS.md`): 100% coherencia en campos detectados
- [x] Implementación del pipeline OCR mínimo
  - `scripts/ocr.py`: PDF → imagen PNG (pypdfium2, 300 DPI configurable)
  - `iniciar_ocr.bat`: lanza `python.exe scripts/ocr.py`
  - `scripts/__init__.py`: paquete de `scripts/`
- [x] Prueba de humo con `solicitude-001.pdf` (2473 × 3378 px, A4 a 300 DPI)
- [x] Repositorio GitHub privado (`https://github.com/alfonsodiz/autHovaes`) con implementación mínima
- [x] Commit `28722d4`: «Pipeline OCR mínimo: PDF -> imagen con pypdfium2 (300 DPI)»

## En curso

- [ ] Probar los dos PDFs restantes (`solicitude-002`, `solicitude-003`) y verificar visualmente la rasterización de `scripts/ocr.py`.
- [ ] Integrar PaddleOCR-json en el pipeline (imagen → texto OCR).
- [ ] Normalización de texto.
- [ ] Matching territorial (Levenshtein + validación por prefijo INE).
- [ ] Contrato JSON (`DATA_MODEL.md` como fichero, no solo como documento).
- [ ] Extensión Chrome (`manifest.json`, `background.js`, `content.js`).
- [ ] Baseline con PDFs reales (`OCR_VALIDATION.md`).
- [ ] Mapeo `codAnoAcademico` → año (pendiente de recibir el JSON del formulario).

## Pendiente

- [ ] Licencia del proyecto (o confirmar que se mantiene sin licencia).
- [ ] (A medio plazo) Extractor propio del Nomenclátor para sustituir el catálogo de Hovaes (escenario C).

## Riesgos

- Precisión OCR en manuscrito (estudio externo: menos del 30% con PaddleOCR; probable reformulación como «pre-relleno asistido con revisión total»).
- Encoding UTF-8 sin BOM: lectura explícita obligatoria.
- 23 duplicados de parroquia/lugar requieren desambiguación por el usuario.
- Licencia del catálogo original no confirmada. Mitigación: catálogo fuera del repo; sustitución a medio plazo por extracto del Nomenclátor.
- Carga dinámica de los selects del formulario: la extensión debe esperar y disparar `change` en cascada.
- HTTP local: bind solo a `127.0.0.1`, CORS estricto, token compartido (ver ADR-001).
- Prueba visual pendiente de los PDFs `solicitude-002` y `solicitude-003`.