# ADR-003: Extracción PDF -> imagen

## Estado

Aceptado.

## Contexto

El pipeline OCR necesita convertir un PDF escaneado (1 hoja, manuscrita) en una imagen rasterizada que se pueda pasar al motor OCR (PaddleOCR-json). El PDF de entrada es la primera hoja de la solicitud ED434A, que contiene los datos de identificación, dirección y datos específicos del procedimiento.

Restricciones aplicables (ver `DEPLOYMENT_CONSTRAINTS.md`):

- Sin admin.
- Sin instalación de sistema.
- Sin PATH.
- Sin variables de entorno.
- Sin registro.
- Python Portable exclusivamente.
- Procesamiento local obligatorio.

El proyecto puede distribuírse fuera del entorno interno, por lo que la licencia de las dependencias es un criterio relevante.

## Alternativas consideradas

### A) PyMuPDF (fitz)

- Licencia **AGPL**.
- Wheel con `fitz.dll`, se copia a `.\recursos\libs\` y se ejecuta desde Python Portable.
- Calidad de rasterizado superior.

### B) pypdfium2

- Licencia **Apache/BSD** (permisiva).
- Wheel con `pdfium.dll`, se copia a `.\recursos\libs\` y se ejecuta desde Python Portable.
- Calidad de rasterizado suficiente para OCR estándar.

### C) Poppler

Descartada. `DEPLOYMENT_CONSTRAINTS.md` prohíbe asumir Poppler instalado, y no hay wheel autocontenido para Windows.

### D) Invocar un binario externo

Descartada. Requiere instalación o PATH, o una dependencia externa no versionada.

## Decisión

**pypdfium2** (Apache/BSD) como rasterizador de PDF.

Motivos:

1. **Licencia limpia**: Apache/BSD no impone obligaciones de copyleft sobre el resto del bundle. PyMuPDF (AGPL) obligaría a liberar el código del bundle completo si el producto se distribuye.
2. **Despliegue compatible con las restricciones**: wheel con `pdfium.dll`, se copia a `.\recursos\libs\`, se ejecuta desde Python Portable. Sin instalación de sistema, sin PATH, sin registro.
3. **Calidad suficiente**: no se ha hecho comparativa empírica contra PyMuPDF en este proyecto. Para rasterizado estándar de documentos escaneados, pypdfium2 es suficiente. Si en la validación con PDFs reales se detectan problemas de calidad, se revisa la decisión.

## Consecuencias

### Positivas

- **Sin riesgo legal** por licencia copyleft.
- **Despliegue autocontenido**: `pdfium.dll` va en `.\recursos\libs\`, sin tocar el sistema.
- **Reproducible**: misma versión de pypdfium2 en todos los equipos.

### Negativas / Riesgos

- **Calidad de rasterizado potencialmente inferior** a PyMuPDF en casos de gráficos complejos (imágenes de fondo, tablas o esquemas). En el caso de uso (formulario manuscrito), el riesgo es bajo, pero no se ha medido.
- **Si el rasterizado es insuficiente** para algún PDF concreto, el OCR fallará en esa zona y los campos correspondientes quedarán en `status: "missing"`. El usuario los rellenará manualmente.
- **Dependencia de una wheel con binario**: si pypdfium2 deja de publicar wheels para Windows, hay que congelar la versión actual o migrar.

## Evidencia

- `DEPLOYMENT_CONSTRAINTS.md`: sin instalación de sistema, Python Portable permitido.
- `OCR_OPTIONS.md`: PaddleOCR-json como motor OCR; el rasterizador debe producir una imagen compatible con él.
- `FORM_ANALYSIS.md` §Alcance del OCR: solo la primera hoja del PDF.

## ADRs relacionados

- ADR-001: runtime OCR (PaddleOCR-json + HTTP local).
- ADR-002: catálogo territorial y matching por niveles.