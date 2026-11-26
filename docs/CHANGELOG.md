# CHANGELOG

## Formato

### YYYY-MM-DD

#### Added

#### Changed

#### Fixed

#### Decisions

## Registro

### 2026-11-26

#### Added

- `docs/validation/MATCHING_BASELINE_MANUSCRITOS.md`: informe de baseline de PDFs manuscritos con análisis de coherencia por campo.
- `docs/sessions/SESSION-006.md`: registro de la sesión 006.

#### Fixed

- (ninguno)

#### Changed

- `docs/HANDOVER.md`: añadidas notas de la sesión 006 (baseline de manuscritos).
- `docs/PROJECT_STATUS.md`: marcado baseline de manuscritos como completado.
- `docs/NEXT_SESSION.md`: añadidas tareas completadas de sesión 006 y riesgos actualizados.
- `docs/validation/MATCHING_ANALYSIS_2.md`: informe de sesión 005 (mecanografiados).

### 2026-11-26

#### Fixed

- `scripts/ocr.py`: reducida tolerancia vertical de `6 * altura_e` a `3 * altura_e` para evitar que una etiqueta coja valores de columnas más abajo (falsos positivos: `nome = AVENIDA`, `parroquia = OURENSE`, `lugar = email`).
- `scripts/ocr.py`: `es_valor_valido` descarta valores de `nomeRepresentante` con menos de 4 caracteres (falso positivo: `nomeRepresentante = ueipa`).

#### Changed

- `docs/HANDOVER.md`: reflejada corrección de falsos positivos y eliminación de problema abierto resuelto.
- `docs/PROJECT_STATUS.md`: añadida corrección de 5 falsos positivos como completado.
- `docs/NEXT_SESSION.md`: eliminadas tareas de corrección de campos (completadas) y añadido registro de tareas completadas.
- `docs/validation/MATCHING_ANALYSIS_2.md`: nuevo informe de comparación antes/después.

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

### 2026-11-20 (mejora del matching por palabras clave)

#### Added

- Variantes en castellano de etiquetas en `scripts/ocr.py` (nombre, primer apellido, segundo apellido, tipo de vía, nombre de la vía, fecha de nacimiento, etc.)
- Tolerancia vertical aumentada (6 × altura_e en lugar de 4 × altura_e) para buscar el valor debajo de la etiqueta
- Validación de formato por campo (`es_valor_valido`): `cp` (5 dígitos), `dni` (8 dígitos + letra), `correo` (contiene @), `dataNacemento` (dd/mm/yyyy), `sexo` (F/M), `anoAcademico` (4 dígitos)
- Lista `ETIQUETAS_FORMULARIO` para descartar etiquetas como valores

#### Changed

- `scripts/ocr.py`: búsqueda de valor desplazada de "misma línea a la derecha" a "debajo de la etiqueta, misma columna"
- `docs/validation/MATCHING_BASELINE_MECANOGRAFADOS.md`: actualizado con resultados tras corrección
- `docs/validation/MATCHING_ANALYSIS.md`: nuevo informe de comparación antes/después
- `docs/HANDOVER.md`: reflejado nuevo estado del matching
- `docs/PROJECT_STATUS.md`: matching por palabras clave marcado como completado
- `docs/NEXT_SESSION.md`: tareas actualizadas con corrección de problemas de asignación

#### Fixed

- `cp` ya no se detecta como `AYUNTAMIENTO` (ahora detecta CP válido: `32500`, `32618`)
- `tipoVia` ya no se detecta como `NOMBRE DE LA VIA` (ahora detecta `AVENIDA`, `Rua`)
- `provincia` ya no se detecta como `AYUNTAMIENTO`

#### Decisions

- Buscar valor debajo de la etiqueta (no a la derecha) para adaptarse a formularios mecanografiados con etiquetas sobre el valor
- Umbral de similitud para `es_etiqueta` mantenido en 0.75 para variantes en castellano
