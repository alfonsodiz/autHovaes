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

### 2026-11-16 (traducción y definición)

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

### 2026-11-16 (implementación del pipeline PDF → imagen)

#### Added

- `scripts/__init__.py` (baleiro, para que `scripts/` sea un paquete).
- `scripts/ocr.py`: pipeline mínimo PDF → imagen. Extrae la primera página del PDF, la rasteriza con pypdfium2 a 300 DPI (configurable como argumento opcional) y guarda un PNG en `recursos/salida/`.
- `iniciar_ocr.bat` en la raíz: lanza `python.exe scripts/ocr.py` con argumentos.
- `sessions/SESSION-003.md`: registro de la sesión de implementación.
- Bundle local (no versionado): Python Portable 3.14 + `pip` + `pypdfium2 5.15.2` + `Pillow` en `recursos/libs/`.

#### Changed

- `.gitignore`: añadidas las reglas `recursos/salida/` y `recursos/pdfs-exemplo/`.
- `HANDOVER.md`: refleja el pipeline PDF → imagen y el commit `28722d4`.
- `PROJECT_STATUS.md`: fase actual «Implementación», no «Definición de arquitectura».
- `NEXT_SESSION.md`: el siguiente paso es integrar PaddleOCR-json, probar los dos PDFs restantes y empezar el matching territorial.

#### Fixed

- (ninguno)

#### Decisions

- Python 3.14 (embeddable) como versión del Python Portable. `pip` instalado con `get-pip.py` + edición de `python314._pth` (`import site` y `Lib\site-packages`).
- Pillow añadido como dependencia explícita (necesario para `bitmap.to_pil()` de pypdfium2).
- DPI por defecto 300, configurable como argumento opcional (`.\iniciar_ocr.bat <pdf> [dpi]`).
- Salida en `recursos/salida/` (relativo al proyecto), no en `%TEMP%`.
- Solo se procesa la primera página del PDF (ver `FORM_ANALYSIS.md` §Alcance del OCR).

#### Pending

- Probar los PDFs `solicitude-002.pdf` y `solicitude-003.pdf`.
- Integrar PaddleOCR-json (imagen → texto OCR).
- Normalización de texto.
- Matching territorial (Levenshtein + validación por prefijo INE).
- Contrato JSON (`DATA_MODEL.md`).
- Extensión Chrome (`manifest.json`, `background.js`, `content.js`).
- Baseline con PDFs reales (`OCR_VALIDATION.md`).
- Mapeo `codAnoAcademico` → año (pendiente de recibir el JSON del formulario).