# AGENTS

## Contexto

Sistema de precarga de formularios web a partir de PDF manuscritos escaneados.

## Restricciones críticas

- Sin privilegios de administrador.
- Sin modificación de PATH.
- Sin modificación de variables de entorno.
- Sin modificación del registro.
- Sin instalación de servicios.
- Python Portable exclusivamente.
- Procesamiento local obligatorio.
- Extensión Chrome/Edge preferente.
- Ejecución de scripts PowerShell bloqueada por GPO de usuario. Ver `architecture/DEVELOPMENT_ENVIRONMENT.md`.

## Restricciones de datos

- El catálogo territorial es `.\recursos\catalogo-hovaes-lugares-galicia-completo.json` (UTF-8 sin BOM). Es la única fuente de matching.
- **Todo acceso a ficheros JSON debe forzar UTF-8 explícito**:
  `[System.IO.File]::ReadAllText($path, [System.Text.UTF8Encoding]::new($false))`.
  No usar `Get-Content -Raw` en PowerShell 5.1 (corrompe tildes y ñ).
- No se generan ni se inventan códigos INE. Vienen del catálogo.
- Las entradas `(descatalogada)` no existen en el catálogo actual. Si se regenera, deben excluirse.

## Lectura obligatoria

1. HANDOVER.md
2. PROJECT_STATUS.md
3. NEXT_SESSION.md
4. Última SESSION-XXX.md

## Cierre obligatorio de sesión

Actualizar:

- HANDOVER.md
- CHANGELOG.md
- PROJECT_STATUS.md
- NEXT_SESSION.md
- SESSION-XXX.md

## Reglas

- Priorizar despliegue frente a sofisticación.
- No introducir dependencias que requieran instalación.
- Documentar todas las decisiones.
- Añadir checklist de validación.
- El sistema no presenta resultados como definitivos. Todo valor OCR requiere revisión del usuario.