# CHANGELOG

## Formato

### YYYY-MM-DD

#### Added

#### Changed

#### Fixed

#### Decisions

## Registro

### 2026-10-26

#### Added

- Catálogo territorial `.\recursos\catalogo-hovaes-lugares-galicia-completo.json`.
- ADR-002: matching por niveles con códigos INE.
- `CATALOGS.md`, `DATA_MODEL.md`, `HOVAES_CATALOG_ANALYSIS.md`, `FORM_ANALYSIS.md`.

#### Decisions

- Provincia derivada por prefijo del concello (`15`, `27`, `32`, `36`).
- «Localidade» como término funcional (nivel de 7 dígitos).
- Descatalogados eliminados en la extracción.
- Duplicados (23) devueltos como candidatos múltiples.

### 2026-11-16

#### Added

- `GLOSARIO.md`: referencia cruzada gallego ↔ castellano ↔ identificador técnico.
- `ADR-001-runtime-ocr.md`: PaddleOCR-json + HTTP local + `.bat` manual + fichero de estado en `%TEMP%`.
- `ADR-003-extraccion-pdf-imaxe.md`: pypdfium2 (Apache/BSD).
- `sessions/SESSION-002.md`: cierre de la sesión de traducción y definición.
- Repositorio GitHub privado `https://github.com/alfonsodiz/autHovaes`.

#### Changed

- Traducción al castellano de los 21 ficheros `.md` de `docs/`.
- Corrección de mojibake en `CATALOGS.md`, `DATA_MODEL.md`, `DEVELOPMENT_ENVIRONMENT.md`.
- `FORM_ANALYSIS.md` ampliado con selectores completos, valores de radios/selects, comportamiento dinámico, bloques Documentación y Comprobación de datos.
- `CATALOGS.md` §Duplicados corregida (parroquia vs lugar, no capital vs entidad).
- `OCR_PIPELINE.md` completado (umbrales, N, duplicados).
- `DEPLOYMENT_CONSTRAINTS.md` actualizado (Native Messaging descartado, HTTP local documentado, bundle permitido).

#### Decisions

- Política de traducción: texto narrativo a castellano; identificadores técnicos, rutas, claves JSON, valores de enum y nombres propios del catálogo sin cambios.
- `concello` se mantiene como galleguismo técnico del dominio (ver `GLOSARIO.md`).
- `localidade` se traduce a «localidad» en el texto; en backticks cuando es identificador.
- Catálogo fuera del repositorio GitHub (escenario B). Sustitución a medio plazo por extracto del Nomenclátor (escenario C).
- pypdfium2 elegido como rasterizador de PDF (licencia limpia, despliegue autocontenido).
- HTTP local (`127.0.0.1`, puerto efímero) como mecanismo de comunicación extensión ↔ proceso Python. Native Messaging descartado por requerir registro.
- `.bat` lanzado manualmente por el usuario; la extensión no lanza procesos.
- Umbrales de similitud: concello ≥ 0.70, localidad ≥ 0.75, lugar ≥ 0.80. N=5 para concello y localidad; todos los lugares que superen el umbral.
- Duplicados presentados como filas separadas, con nombre completo y `codigo` visible.