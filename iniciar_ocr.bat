@echo off
REM Lanza el pipeline OCR.
REM Uso: iniciar_ocr.bat <ruta_al_pdf> [dpi]

setlocal
set SCRIPT_DIR=%~dp0
set PYTHON=%SCRIPT_DIR%recursos\python-portable\python.exe

if not exist "%PYTHON%" (
    echo ERROR: no se encuentra %PYTHON%
    exit /b 1
)

"%PYTHON%" "%SCRIPT_DIR%scripts\ocr.py" %*
exit /b %ERRORLEVEL%