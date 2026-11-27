# CHROME EXTENSION

## Objetivo

Extensión Chrome/Edge (cargada en modo desarrollador) que precarga los valores del JSON generado por el pipeline OCR en el formulario ED434A de la Xunta de Galicia.

**Filosofía**: pre-relleno asistido, no automático. La extensión **nunca** envía el formulario. El usuario revisa y envía manualmente.

## Alcance (Opción A — mínima)

1. Detectar que el usuario está en el formulario ED434A (`Homologacion-inicial.action`).
2. Leer el JSON del proceso Python (por HTTP local o fichero de estado).
3. Precargar los valores en los campos del formulario (por `id`, con espera de carga dinámica y `change` en cascada).
4. No mostrar paneles ni UI adicional. Solo precargar.
5. No enviar el formulario. El usuario revisa y envía.

## Comunicación con el proceso Python

Según ADR-001, la comunicación es por **HTTP local** (`127.0.0.1:<puerto efímero>`).

- El proceso Python abre un socket en `127.0.0.1` (nunca `0.0.0.0`).
- La extensión hace `fetch()` al puerto.
- CORS estricto: solo se acepta el origen `chrome-extension://<id>`.
- Token compartido: la extensión debe enviar un token en cada petición. El proceso rechaza peticiones sin token.
- Fichero de estado en `%TEMP%` con `{puerto, token, pid}`.
- La extensión lee el fichero de estado al arrancar (o al detectar el formulario).

**Nota**: en la fase actual (implementación mínima), la extensión puede leer el JSON **directamente del fichero** `recursos/salida/<pdf>_matching.json`, sin necesidad de HTTP local. La comunicación HTTP local se implementará cuando el proceso Python esté listo para servir peticiones.

## Detección del formulario

La extensión detecta que está en el formulario ED434A por:
- URL: `Homologacion-inicial.action` (o similar).
- DOM: presencia del formulario `#formularioHomologacion`.

## Precarga de valores

Para cada campo del JSON (`fields`), la extensión:

1. Busca el elemento del formulario por `id` (según `form_id` del JSON, o según el mapeo de `FORM_ANALYSIS.md`).
2. Espera a que el elemento esté cargado (los `select` de concello/localidade/lugar se cargan por AJAX).
3. Setea el valor:
   - Para `input` de texto: `element.value = valor`.
   - Para `select`: busca la `option` con `value` igual al `codigo` (para provincia, concello, localidad, lugar) o al texto normalizado (para otros selects).
   - Para `radio`: selecciona el radio correspondiente.
4. Dispara un evento `change` para que el formulario reaccione (p. ej. cargar concellos al cambiar provincia).

## Orden de precarga

Los campos tienen dependencias:
1. Primero `provincia` (dispara carga de concellos).
2. Esperar a que los concellos estén cargados.
3. Luego `concello` (dispara carga de localidades).
4. Esperar a que las localidades estén cargadas.
5. Luego `localidad` (dispara carga de lugares).
6. Esperar a que los lugares estén cargados.
7. Luego `lugar`.
8. Luego el resto de campos (nombre, apellidos, DNI, dirección, etc.).

## Token CSRF

El formulario incluye un token CSRF en la URL (`?OWASP_CSRFTOKEN=...`) y en un `<input type="hidden">`. La extensión **no necesita** el token para precargar valores (solo para enviar el formulario, que no hace).

## Estructura de la extensión

extension/
├── manifest.json      # MV3
├── background.js      # Service worker: lee el JSON, lo envía al content script
├── content.js         # Content script: detecta el formulario, precarga los valores
└── popup.html         # (opcional) UI para seleccionar el JSON a precargar


## Permisos necesarios

- `activeTab` o `scripting` (para inyectar el content script).
- `storage` (para guardar el JSON seleccionado).
- `host_permissions`: `https://www.edu.xunta.gal/*` (para el formulario).

## Pendiente

- Implementar la extensión (manifest, background, content).
- Probar con el formulario real.
- Integrar la comunicación HTTP local con el proceso Python (cuando esté listo).