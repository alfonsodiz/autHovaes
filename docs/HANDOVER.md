# HANDOVER

## Situación actual

Arquitectura cerrada. Catálogo territorial cargado y analizado. Documentación traducida al castellano.

## Último trabajo realizado

- Definición del contrato JSON de salida (`DATA_MODEL.md`).
- Análisis del catálogo territorial (`CATALOGS.md`, `HOVAES_CATALOG_ANALYSIS.md`).
- Observación del comportamiento del formulario ED434A (`FORM_ANALYSIS.md`).
- ADR-002 escrito: matching por niveles con códigos INE.
- Traducción al castellano de los 21 ficheros `.md` de `docs/`.
- Corrección de mojibake en `CATALOGS.md`, `DATA_MODEL.md` y `DEVELOPMENT_ENVIRONMENT.md`.
- Creación de `GLOSARIO.md`.

## Problemas abiertos

- Runtime del OCR sin decidir (ADR-001 pendiente, ver `SESSION-001.md` §Próximos pasos).
- Extracción PDF → imagen sin decidir (ADR-003 pendiente).
- Mecanismo de comunicación extensión ↔ proceso Python sin decidir (consecuencia de ADR-001; ver `DEPLOYMENT_CONSTRAINTS.md` §Contradicciones conocidas).
- Licencia del catálogo original no confirmada.
- Precisión OCR en manuscrito (riesgo: menos del 30% con PaddleOCR según estudio externo).

## Próxima acción recomendada

Escribir ADR-003 (extracción PDF → imagen) y ADR-001 (runtime OCR, corto porque la decisión está tomada en `OCR_OPTIONS.md`).

## Estado

LISTO PARA CONTINUAR