# PROJECT STATUS

## Fase actual

Definición de arquitectura cerrada. Catálogo cargado y analizado. Documentación en castellano.

## Completado

- [x] Estructura documental
- [x] Catálogo territorial cargado y analizado (317 concellos, 3.790 localidades, 34.164 lugares)
- [x] Decisión de matching por niveles (ADR-002)
- [x] Contrato JSON de salida definido (`DATA_MODEL.md`)
- [x] Comportamiento del formulario ED434A observado (`FORM_ANALYSIS.md`)
- [x] Traducción al castellano de los 21 ficheros `.md`
- [x] Corrección de mojibake en `CATALOGS.md`, `DATA_MODEL.md`, `DEVELOPMENT_ENVIRONMENT.md`
- [x] `GLOSARIO.md` creado

## En curso

- [ ] Definición del runtime OCR (ADR-001)
- [ ] Definición de la extracción PDF → imagen (ADR-003)
- [ ] Definición del pipeline de matching detallado (`OCR_PIPELINE.md`)

## Pendiente

- [ ] OCR manuscrito (motor y validación baseline)
- [ ] Extensión Chrome (UI y precarga)
- [ ] Selectores del formulario ED434A
- [ ] Validación con PDFs reales
- [ ] Licencia del catálogo original

## Riesgos

- Precisión OCR en manuscrito (estudio externo: menos del 30% con PaddleOCR; probable reformulación como «pre-relleno asistido con revisión total»).
- Encoding UTF-8 sin BOM: lectura explícita obligatoria.
- 23 duplicados de capital/entidad requieren desambiguación por el usuario.
- Licencia del catálogo original no confirmada.