# GLOSARIO

Referencia cruzada entre los términos del dominio en gallego (usados por el formulario ED434A y por el catálogo), su traducción al castellano en la documentación, y el identificador técnico que aparece en el código, en el JSON y en los selectores del formulario.

## Niveles territoriales

| Gallego (dominio) | Castellano (documentación) | Identificador técnico |
|---|---|---|
| provincia | provincia | `provincia` |
| concello | concello (ver nota) | `concello` |
| localidade | localidad | `localidade` |
| lugar | lugar | `lugar` |
| parroquia | parroquia | (no usado como identificador) |

### Nota sobre «concello»

El término gallego **concello** se mantiene en la documentación en castellano porque:

1. Es el término que usa el formulario ED434A (campo `concello`).
2. Es la clave del catálogo territorial.
3. Es el identificador técnico (`concello`, `filtroCodProvincia`, etc.).

Traducirlo a «municipio» rompería la correspondencia con el formulario, con el catálogo y con el contrato JSON. Se acepta como galleguismo técnico del dominio, igual que se aceptan `localidade` o `filtroCodLocalidade` en contextos donde son identificadores.

### Nota sobre «localidade»

En el texto narrativo se traduce a **localidad**. Cuando se refiere al campo del formulario o a la clave JSON, se escribe en backticks: `localidade`. En el nivel de 7 dígitos corresponde funcionalmente a la **parroquia** del Nomenclátor.

## Códigos INE

| Nivel | Dígitos | Ejemplo |
|---|---|---|
| Provincia | 2 | `15` |
| Concello | 5 | `15001` |
| Localidade | 7 | `1500101` |
| Lugar | 9 | `150010100` |

La provincia no está almacenada en el catálogo; se deriva de los dos primeros dígitos del código de concello (`15`, `27`, `32`, `36`).

## Términos técnicos que no se traducen

Se mantienen en su forma original por ser nombres propios, marcas o identificadores:

- Motores y librerías: `PaddleOCR-json`, `PaddleOCR`, `PyMuPDF`, `pypdfium2`, `Levenshtein`, `Tesseract`, `EasyOCR`, `TrOCR`, `Florence-2`, `Ollama`.
- Formatos y protocolos: `UTF-8 sin BOM`, `Native Messaging`, `HTTP local`, `stdin/stdout`, `subprocess`, `JSON`.
- Entornos y herramientas: `PowerShell 5.1`, `GPO`, `HKCU`, `PATH`.
- Ficheros y rutas: `AGENTS.md`, `HANDOVER.md`, `catalogo-hovaes-lugares-galicia-completo.json`, `scripts/ocr.py`, etc.
- Claves JSON: `fields`, `matching`, `codigo`, `nome`, `confidence`, `bbox`, `raw_text`, `status`, `candidates`, `provincia`, `concello`, `localidade`, `lugar`, `version`, `source_pdf`, `pages`.
- Valores de enum: `review`, `missing`.
- Nombres propios del catálogo: `Abegondo`, `Betanzos`, `Coruña (A)`, etc.
- Códigos INE: `15001`, `1500101`, `150010100`, etc.

## Reglas de estilo

1. Texto narrativo → castellano.
2. Identificadores técnicos, rutas, claves JSON, valores de enum, comandos → sin cambios.
3. Términos del dominio que coinciden con el formulario o el catálogo → castellano en el texto, en backticks cuando son identificadores.
4. Nombres propios del catálogo → sin cambios.