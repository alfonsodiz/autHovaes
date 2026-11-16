# ADR-001: Runtime OCR y comunicación con la extensión

## Estado

Aceptado.

## Contexto

El motor OCR ya está decidido en `OCR_OPTIONS.md`: **PaddleOCR-json (C++)** como único motor, por restricciones de despliegue y rendimiento. Esta ADR no reabre esa decisión; la registra y resuelve lo que faltaba: **cómo se ejecuta y cómo se comunica con la extensión Chrome/Edge**.

Restricciones aplicables (ver `DEPLOYMENT_CONSTRAINTS.md`):

- Sin admin.
- Sin instalación de sistema.
- Sin PATH.
- Sin variables de entorno.
- Sin registro.
- Python Portable exclusivamente.
- Procesamiento local obligatorio.
- Extensión Chrome/Edge en modo desarrollador.

## Decisión

### Motor OCR

**PaddleOCR-json (C++)** como subprocess. Modelos incluidos en el bundle (`.\recursos\paddleocr-json\`). Ver `OCR_OPTIONS.md` para la comparativa de motores.

### Mecanismo de comunicación extensión ↔ proceso Python

**HTTP local** en `127.0.0.1:<puerto efímero>`.

- El proceso Python Portable abre un socket en `127.0.0.1` (nunca `0.0.0.0`).
- La extensión hace `fetch()` al puerto.
- CORS estricto: solo se acepta el origen `chrome-extension://<id>`.
- Token compartido: la extensión debe enviar un token en cada petición. El proceso rechaza peticiones sin token.

### Lanzamiento del proceso

**Manual, por el usuario**, mediante `iniciar_ocr.bat`.

Motivo: la extensión Chrome no puede lanzar procesos directamente. Native Messaging permitiría que Chrome lanzara el proceso, pero **requiere escribir en el registro** (clave en `HKCU`), lo que viola la restricción dura «sin modificación del registro».

### Descubrimiento del puerto y del token

El proceso Python, al arrancar, escribe un fichero de estado en `%TEMP%` con:
