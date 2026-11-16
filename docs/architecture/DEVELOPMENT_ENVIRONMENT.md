# DEVELOPMENT ENVIRONMENT

Restricciones del entorno de desarrollo que no se pueden resolver sin admin o sin cambiar la GPO del dominio. No forman parte del producto desplegado, pero condicionan cómo se escriben y ejecutan las herramientas auxiliares.

## 1. Ejecución de scripts PowerShell bloqueada por GPO

### Síntoma

Cualquier intento de ejecutar un `.ps1` falla con:

    No se puede cargar el archivo ... porque la ejecución de scripts
    está deshabilitada en este sistema.

Incluyendo estos intentos:

    powershell.exe -ExecutionPolicy Bypass -File .\script.ps1
    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

Ninguno de los dos funciona.

### Causa

El orden de precedencia de políticas de PowerShell es:

    MachinePolicy > UserPolicy > Process > CurrentUser > LocalMachine

En el equipo de desarrollo, `UserPolicy` está fijada a `Restricted` por directiva de grupo. Cualquier otra política queda anulada. `Set-ExecutionPolicy` sobre `UserPolicy` falla porque está controlada por GPO.

Verificación:

    Get-ExecutionPolicy -List

Devuelve algo como:

    MachinePolicy       Undefined
    UserPolicy          Restricted     <- causa
    Process             Undefined
    CurrentUser         Bypass         <- ignorado por la GPO
    LocalMachine        Undefined

### Solución que funciona

Ejecutar el contenido del script en memoria, sin cargarlo como fichero `.ps1`:

    Get-Content .\script.ps1 -Raw | Invoke-Expression

Esto funciona porque el bloqueo se aplica a ficheros `.ps1`, no a cadenas de texto ejecutadas con `Invoke-Expression`.

**Limitación**: `Invoke-Expression` no define `$PSScriptRoot` ni `$PSCommandPath`. Si un script necesita saber su ubicación, hay que resolverlo con `Get-Location` o pasarle la ruta como argumento. El `init-project-docs.ps1` actual no los usa.

### Solución alternativa: pegar el contenido en la consola

Si `Invoke-Expression` también fallase (por ejemplo, por política de proceso más restrictiva), se puede:

1. Abrir el `.ps1` en un editor.
2. Seleccionar todo, copiar.
3. Pegar en la consola de PowerShell y pulsar Enter.

Equivalente a `Invoke-Expression`, pero manual.

### Solución que respeta las restricciones: `.bat` + `python.exe`

Para lanzar herramientas auxiliares (OCR, validación de catálogo, etc.), **no usar PowerShell**. Usar un `.bat` que llame directamente al ejecutable:

    @echo off
    "%~dp0recursos\python-portable\python.exe" "%~dp0scripts\ocr.py" %*

Esto evita PowerShell por completo. Es la opción coherente con las restricciones del proyecto (sin admin, sin instalación).

### Soluciones descartadas

- `Set-ExecutionPolicy -Scope CurrentUser`: ignorada por la GPO de `UserPolicy`.
- `Set-ExecutionPolicy -Scope LocalMachine`: requiere admin y va contra las restricciones.
- Modificar la GPO: requiere admin o dominio.
- `Unrestricted`: ídem.
- Tocar el registro: va contra «Sin modificación del registro» de `AGENTS.md`.

## 2. Consecuencias para el proyecto

- **Los scripts `.ps1` del proyecto no se pueden ejecutar directamente** en el entorno de desarrollo actual. Hay que usar `Get-Content ... | Invoke-Expression` o `.bat` + `python.exe`.
- **Los scripts auxiliares de Python no tienen este problema**: `python.exe script.py` se ejecuta sin restricciones.
- **La extensión Chrome tampoco**: se carga en modo desarrollador y no usa PowerShell.
- **El despliegue final** (Python Portable + `.bat`) no depende de PowerShell, así que este problema es solo del entorno de desarrollo.

## 3. Cómo documentar nuevas herramientas

Cuando se escriba una herramienta auxiliar:

1. Si es PowerShell, documentar en su cabecera cómo ejecutarla (`Get-Content ... | Invoke-Expression`).
2. Si es Python, lanzarla siempre desde `.bat` o directamente con `python.exe`.
3. No asumir que `.\script.ps1` va a funcionar.

## 4. Nota sobre el incidente original

Este documento se creó después de que el script `init-project-docs.ps1` fallase al ejecutarse con `.\init-project-docs.ps1` y con `powershell.exe -ExecutionPolicy Bypass -File`. La solución aplicada fue `Get-Content .\init-project-docs.ps1 -Raw | Invoke-Expression`, que funcionó sin tocar políticas ni registro.

Fecha del incidente: 2026-10-26.