# HANDOVER

## Situación actual

Arquitectura cerrada. Documentación en castellano. Repositorio GitHub privado inicializado. ADR-001 y ADR-003 escritos. `OCR_PIPELINE.md` completado.

## Último trabajo realizado

- Traducción al castellano de los 21 ficheros `.md` de `docs/`.
- Corrección de mojibake en `CATALOGS.md`, `DATA_MODEL.md`, `DEVELOPMENT_ENVIRONMENT.md`.
- `GLOSARIO.md` creado.
- `FORM_ANALYSIS.md` ampliado con selectores completos, valores de radios/selects, comportamiento dinámico, bloques Documentación y Comprobación de datos.
- `CATALOGS.md` §Duplicados corregida (parroquia vs lugar, no capital vs entidad).
- ADR-003: pypdfium2 para extracción PDF -> imagen.
- ADR-001: PaddleOCR-json como motor único; HTTP local como mecanismo de comunicación; `.bat` lanzado manualmente por el usuario; fichero de estado en `%TEMP%`.
- `DEPLOYMENT_CONSTRAINTS.md` actualizado (Native Messaging descartado, HTTP local documentado).
- `OCR_PIPELINE.md` completado (umbrales 0.70/0.75/0.80, N=5, duplicados como filas separadas).
- Repositorio GitHub privado `https://github.com/alfonsodiz/autHovaes` inicializado con 26 ficheros (3 raíz + 22 `.md` + `.gitkeep`). Catálogo y binarios fuera del repo.

## Problemas abiertos

- Mapeo `codAnoAcademico` -> año (pendiente de recibir el JSON del formulario).
- Licencia del catálogo original (mitigación: fuera del repo; sustitución a medio plazo por Nomenclátor).
- Precisión OCR en manuscrito (riesgo: menos del 30% con PaddleOCR).
- Carga dinámica de los selects del formulario: la extensión debe esperar y disparar `change` en cascada.

## Próxima acción recomendada

Implementar el esqueleto del pipeline OCR (`scripts/ocr.py`, `iniciar_ocr.bat`) y de la extensión Chrome (`manifest.json`, `background.js`, `content.js`). Ver `NEXT_SESSION.md`.

## Estado

LISTO PARA CONTINUAR