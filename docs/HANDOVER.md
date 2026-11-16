# HANDOVER

## Situación actual

Implementación activa. La fase de definición de arquitectura está cerrada: todas las ADR están escritas y el pipeline OCR mínimo (PDF → imagen) está funcionando. La extensión Chrome aún no está implementada y la integración de PaddleOCR-json no se ha iniciado.

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

## Problemas abiertos

- Prueba visual pendiente de los PDFs `solicitude-002` y `solicitude-003`.
- Integración de PaddleOCR-json en el pipeline (imagen → texto OCR).
- Normalización de texto.
- Matching territorial (Levenshtein + validación por prefijo INE).
- Contrato JSON (`DATA_MODEL.md` como fichero).
- Extensión Chrome (`manifest.json`, `background.js`, `content.js`) — precarga por `codigo`, espera de carga dinámica y `change` en cascada.
- Baseline con PDFs reales (`OCR_VALIDATION.md`).
- Mapeo `codAnoAcademico` → año (pendiente de recibir el JSON del formulario).

## Próxima acción recomendada

Continuar la implementación:
1. Probar los dos PDFs restantes y verificar visualmente.
2. Integrar PaddleOCR-json (imagen → texto OCR).
3. Normalización de texto.
4. Matching territorial.
5. Extensión Chrome.
6. Baseline con PDFs reales.

## Estado

LISTO PARA CONTINUAR