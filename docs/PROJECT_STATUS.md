# PROJECT STATUS

## Fase actual

Definición de arquitectura cerrada. Documentación en castellano. Repositorio GitHub privado inicializado (`https://github.com/alfonsodiz/autHovaes`). Catálogo fuera del repo (escenario B).

## Completado

- [x] Estructura documental
- [x] Catálogo territorial cargado y analizado (317 concellos, 3.790 localidades, 34.164 lugares)
- [x] Decisión de matching por niveles (ADR-002)
- [x] Contrato JSON de salida definido (`DATA_MODEL.md`)
- [x] Comportamiento del formulario ED434A observado y selectores documentados (`FORM_ANALYSIS.md`)
- [x] Traducción al castellano de los 21 ficheros `.md`
- [x] Corrección de mojibake en `CATALOGS.md`, `DATA_MODEL.md`, `DEVELOPMENT_ENVIRONMENT.md`
- [x] `GLOSARIO.md` creado
- [x] ADR-003: extracción PDF -> imagen (`pypdfium2`)
- [x] ADR-001: runtime OCR (PaddleOCR-json) y mecanismo de comunicación (HTTP local + `.bat`)
- [x] `OCR_PIPELINE.md` completado (umbrales, N, duplicados)
- [x] Repositorio GitHub privado inicializado con documentación

## En curso

- [ ] Implementación del pipeline OCR (`scripts/ocr.py`, `iniciar_ocr.bat`)
- [ ] Implementación de la extensión Chrome (`manifest.json`, `background.js`, `content.js`)

## Pendiente

- [ ] Baseline de OCR con PDFs reales
- [ ] Selectores de la extensión: espera de carga dinámica y disparo de `change` en cascada
- [ ] Mapeo `codAnoAcademico` -> año (pendiente de recibir el JSON)
- [ ] Licencia del proyecto (o confirmar que se mantiene sin licencia)
- [ ] (A medio plazo) Extractor propio del Nomenclátor para sustituir el catálogo de Hovaes (escenario C)

## Riesgos

- Precisión OCR en manuscrito (estudio externo: menos del 30% con PaddleOCR; probable reformulación como «pre-relleno asistido con revisión total»).
- Encoding UTF-8 sin BOM: lectura explícita obligatoria.
- 23 duplicados de parroquia/lugar requieren desambiguación por el usuario.
- Licencia del catálogo original no confirmada. Mitigación: catálogo fuera del repo; sustitución a medio plazo por extracto del Nomenclátor.
- Carga dinámica de los selects del formulario: la extensión debe esperar y disparar `change` en cascada.
- HTTP local: bind solo a `127.0.0.1`, CORS estricto, token compartido (ver ADR-001).