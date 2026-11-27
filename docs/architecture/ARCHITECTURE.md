# ARCHITECTURE

## Pipeline

    PDF
     |
     v
    Alineamiento
     |
     v
    Recorte
     |
     v
    OCR
     |
     v
    Normalización de texto
     |
     v
    Matching territorial (por niveles)
       provincia -> concello -> localidad -> lugar
       validación por prefijo INE
     |
     v
    JSON
     |
     v
    Extensión Chrome
       precarga por código INE
     |
     v
    Formulario ED434A

## Notas

- El matching es por niveles: nunca se compara el OCR contra los 34.164 lugares. Solo dentro de la localidad elegida (5-20 candidatos típicos).
- La extensión precarga por `codigo` cuando el formulario expone códigos INE en los `option value`. Si no, por `nome` normalizado (con riesgo de error).
- Ver `OCR_PIPELINE.md` para el detalle del matching, y `CATALOGS.md` para la estructura del catálogo.

## Extensión Chrome

La extensión Chrome/Edge (cargada en modo desarrollador) precarga los valores del JSON en el formulario ED434A. **No envía el formulario**: el usuario revisa y envía manualmente. Ver `CHROME_EXTENSION.md` para el detalle.