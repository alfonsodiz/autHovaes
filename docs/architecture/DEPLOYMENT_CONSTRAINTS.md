# DEPLOYMENT CONSTRAINTS

## Obligatorio

- Sin admin.
- Sin instalación.
- Sin PATH.
- Sin variables de entorno.
- Sin registro.

## Permitido

- Python Portable.
- Chrome / Edge.
- Extensión Chrome/Edge (cargada en modo desarrollador).
- Bundle autocontenido en `.\recursos\`: `python-portable\`, `paddleocr-json\`, `libs\` (pypdfium2).
- Extensión Chrome/Edge (cargada en modo desarrollador). Ver `CHROME_EXTENSION.md`.

## Prohibido asumir

- Docker
- NodeJS
- Redis
- PostgreSQL
- Tesseract instalado
- Poppler instalado

## Contradicciones conocidas

- **Extensión Chrome ↔ «sin instalación»**: cargar una extensión en modo desarrollador no es instalación de sistema, pero hay que documentarlo.
- **Native Messaging**: descartado. Requiere clave en `HKCU`, lo que contradice «sin registro». Ver ADR-001 para el mecanismo elegido (HTTP local).

## Mecanismo de comunicación extensión ↔ proceso Python

**HTTP local** en `127.0.0.1:<puerto efímero>`. Ver ADR-001.

- Sin registro, sin admin, sin instalación.
- Bind solo a `127.0.0.1`.
- CORS estricto (`chrome-extension://<id>`).
- Token compartido.
- Fichero de estado en `%TEMP%` con `{puerto, token, pid}`.

## Lanzamiento del proceso Python

**Manual**, por el usuario, mediante `iniciar_ocr.bat`. La extensión no puede lanzar procesos directamente (sin Native Messaging). Ver ADR-001.

