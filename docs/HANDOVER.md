# HANDOVER

## Situación actual

Implementación activa. Fase de arquitectura cerrada (ADR-001, ADR-002, ADR-003). Pipeline OCR completo funcionando: PDF → imagen (pypdfium2) → OCR (PaddleOCR-json) → matching por palabras clave → matching territorial (Levenshtein + validación por prefijo INE sobre el catálogo de Galicia, umbral de corrección 0.80) → JSON en UTF-8 sin BOM. La extensión Chrome aún no está implementada.

## Último trabajo realizado

- Decisiones arquitectónicas publicadas:
  - **ADR-003**: pypdfium2 (Apache/BSD) como rasterizador de PDF (descartado PyMuPDF por riesgo AGPL).
  - **ADR-001**: PaddleOCR-json como motor OCR + HTTP local (`127.0.0.1:puerto efímero`) como mecanismo de comunicación; Native Messaging descartado por requerir registro (`HKCU`).
- Implementación del pipeline OCR mínimo:
  - `scripts/ocr.py`: PDF → imagen PNG con pypdfium2 (300 DPI configurable).
  - `iniciar_ocr.bat`: lanza `python.exe scripts/ocr.py` manualmente.
  - `scripts/__init__.py`: paquete.
  - `recursos/libs/`: `pypdfium2 5.15.2`, `Pillow` (instalados con `pip install --target`).
  - `recursos/python-portable/`: Python Portable 3.14, con `pip` e `import site` activado.
- Prueba de humo: `.\iniciar_ocr.bat recursos\pdfs-exemplo\solicitude-001.pdf` → `C:\autHovaes\recursos\salida\solicitude-001_p1.png` (2473 × 3378 px, correcto).
- `.gitignore` actualizado: `recursos/salida/` y `recursos/pdfs-exemplo/`.
- Commit `28722d4`: «Pipeline OCR mínimo: PDF -> imagen con pypdfium2 (300 DPI)».
- Repositorio GitHub privado sincronizado: `https://github.com/alfonsodiz/autHovaes`.
- Catálogo (`catalogo-hovaes-lugares-galicia-completo.json`), binarios y PDFs de ejemplo fuera del repo (ignorados).
- Sesión 007: matching territorial implementado en `scripts/ocr.py` y ejecutado sobre los 5 PDFs de ejemplo (informe en `docs/validation/MATCHING_TERRITORIAL_ANALYSIS.md`).

## Problemas abiertos

- Extensión Chrome (`manifest.json`, `background.js`, `content.js`) — precarga por `codigo`, espera de carga dinámica y `change` en cascada.
- Baseline con PDFs reales (`OCR_VALIDATION.md`).
- Mapeo `codAnoAcademico` → año (pendiente de recibir el JSON del formulario).
- Prueba visual de los PDFs `solicitude-002` y `solicitude-003`.
- Licencias (proyecto y catálogo original de Hovaes).

## Próxima acción recomendada

Continuar la implementación:
1. Extensión Chrome.
2. Baseline con PDFs reales.
3. Mapeo `codAnoAcademico` → año.

## Estado

LISTO PARA CONTINUAR

## Notas de la sesión 006

- Baseline de PDFs manuscritos ejecutado y analizado (`manuscrito-001`, `manuscrito-002`, `manuscrito-003`).
- Tasa de coherencia ~49% con manuscritos (frente al ~84-92% con mecanografiados).
- Campos que más fallan: `nome`/`apelidos`, `provincia`/`concello`/`localidade`, `correo`, `tipoVia`/`nomeVia`.
- Campos casi no detectados: `dni`, `cp`, `dataNacemento`, `telefono`.
- Informe: `docs/validation/MATCHING_BASELINE_MANUSCRITOS.md`.

## Notas de la sesión 005

- Corregidos 5 falsos positivos en `scripts/ocr.py`:
  - **Corrección A**: tolerancia vertical reducida de `6 * altura_e` a `3 * altura_e` (línea 430).
  - **Corrección B**: `es_valor_valido` descarta `nomeRepresentante` con menos de 4 caracteres (líneas 324-325).
- Verificado con ambos PDFs mecanografiados (`mecanografiado-001`, `mecanografiado-002`).
- Informe: `docs/validation/MATCHING_ANALYSIS_2.md`.

## Notas de la sesión 007

- Matching territorial implementado y ejecutado sobre los 5 PDFs de ejemplo.
- manuscritoi-001: concello "ourense" y localidade "oorense" corregidos a "Ourense" (32054 / 3205400); provincia "3204" corregida a "Ourense" (32). Confianza 0.8571.
- manuscritoi-002 y 003: sin cambios (OCR demasiado desviado o sin concello detectado; no se introduce ruido).
- mecanografiado-001: sin cambio automático (mejor candidato "O Carballiño" ≈ 0.818 < 0.85).
- mecanografiado-002: coincidencia exacta (Monterrei 32050 / San Cristovo 320500901), confianza 1.0, prefijos INE validados.
- Informe: `docs/validation/MATCHING_TERRITORIAL_ANALYSIS.md`.

## Notas de la sesión 008

- Ajuste del umbral de corrección del matching territorial de 0.85 a 0.80 en `scripts/ocr.py` (`UMBRAL_ACEPTAR_CONCELLO`, `UMBRAL_ACEPTAR_LOCALIDADE`, `UMBRAL_ACEPTAR_LUGAR`).
- Reejecutado el pipeline sobre los 5 PDFs de ejemplo.
- mecanografiado-001: concello "CARBALLINO," corregido a "Carballiño (O)" (32019), score 0.8333 ≥ 0.80; provincia derivada "Ourense" (32). Antes (0.85) no se corregía (score ≈ 0.818 < 0.85).
- manuscrito-001: sin cambios (ya corregido con 0.85).
- manuscrito-002 y 003: sin cambios (OCR demasiado desviado).
- mecanografiado-002: sin cambios (coincidencia exacta, confianza 1.0).
- Ningún campo empeorado; no se detectaron falsos positivos.
- Informe: `docs/validation/MATCHING_TERRITORIAL_ANALYSIS_2.md`.