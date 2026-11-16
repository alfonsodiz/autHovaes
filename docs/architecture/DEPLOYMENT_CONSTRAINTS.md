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

## Prohibido asumir

- Docker
- NodeJS
- Redis
- PostgreSQL
- Tesseract instalado
- Poppler instalado

## Contradicciones conocidas

- **Native Messaging <-> registro**: la comunicación entre extensión Chrome y proceso nativo local requiere clave en `HKCU`. Pendiente de decisión (ver ADR-001).
- **Extensión Chrome <-> «sin instalación»**: cargar una extensión en modo desarrollador no es instalación de sistema, pero hay que documentarlo.