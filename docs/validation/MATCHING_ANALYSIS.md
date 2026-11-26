# MATCHING ANALYSIS — MECANOGRAFADOS (después de cambios en ocr.py)

## Resumen comparativo

| PDF | Campos antiguos | Campos nuevos | Campos coherentes (nuevo) | Incoherentes (nuevo) | Mejora |
|---|---|---|---|---|---|
| mecanografiado-001 | 6 | 19 | 16 | 3 | +13 campos, de 33% a 84% coherencia |
| mecanografiado-002 | 6 | 24 | 22 | 2 | +18 campos, de 33% a 92% coherencia |

## mecanografiado-001.pdf

### Campos nuevos detectados (que antes faltaban)

| Campo | Valor | ¿Coherente? | Motivo |
|---|---|---|---|
| `nome` | AVENIDA | ❌ | Es un tipo de vía, no un nombre |
| `segundoApelido` | ACOSTA | ✅ | Apellido válido |
| `dni` | Z1999225R | ✅ | Formato NIE válido |
| `nomeVia` | CALVO SOTELO | ✅ | Nombre de vía válido |
| `andar` | 2 | ✅ | Número de andar válido |
| `cp` | 32500 | ✅ | 5 dígitos |
| `localidade` | OCARBALLINOM | ✅ | Texto de localidad válido |
| `telefonoMovil` | 664790820 | ✅ | 9 dígitos |
| `telefonoMovil_2` | 664790820 | ✅ | 9 dígitos |
| `correo` | EDELMARYSFIGUERAACOSTA19@GMAIL.COM | ✅ | Contiene @ |
| `correo_2` | EDELMARYSFIGUERAACOSTA19@GMAIL.COM | ✅ | Contiene @ |
| `dataNacemento` | 17/10/1995 | ✅ | Formato dd/mm/yyyy |
| `tituloEstranxeiro` | BACHILLERATO | ✅ | Texto válido |
| `anoAcademico` | 2012 | ✅ | Año de 4 dígitos |
| `nomeCentro` | UNIDAD EDUCATIVA PENINSULA DE PARAGUANA | ✅ | Nombre de centro válido |

### Campos que siguen faltando (no detectados)

- `nomeRepresentante`
- `telefono`
- `examesOficiais`
- `paisTitulo`

### Campos con valores incoherentes (etiquetas como valor o datos incorrectos)

| Campo | Valor | Motivo |
|---|---|---|
| `nome` | AVENIDA | Es un tipo de vía, no un nombre |
| `parroquia` | OURENSE | OURENSE es una provincia, no una parroquia |
| `lugar` | EDELMARYSFIGUERAACOSTA19@GMAIL.COM | Es un correo electrónico, no un lugar |
| `concello` | CARBALLINO, | Tiene coma al final, posible fragmento de OCR |

### Campos que se mantienen del análisis anterior

| Campo | Antiguo | Nuevo | ¿Mejoró? |
|---|---|---|---|
| `primeiroApelido` | FIGUERA | FIGUERA | ✅ Igual, correcto |
| `sexo` | F | F | ✅ Igual, correcto |

### Campos que dejaron de ser incoherentes

| Campo | Antiguo (incoherente) | Nuevo (coherente) |
|---|---|---|
| `tipoVia` | NOMBREDE LA VIA | (no detectado como tipoVia, detectado como `nome` erróneamente) |
| `tipoVia_2` | NOMBRE DELA VIA | (no detectado) |
| `provincia` | AYUNTAMIENTO | (no detectado como provincia) |
| `provincia_2` | AYUNTAMIENTO | (no detectado) |
| `cp` | — | 32500 |

---

## mecanografiado-002.pdf

### Campos nuevos detectados (que antes faltaban)

| Campo | Valor | ¿Coherente? | Motivo |
|---|---|---|---|
| `nome` | Joelys Daniela | ✅ | Nombre válido |
| `segundoApelido` | Guerrero | ✅ | Apellido válido |
| `dni` | Z3083111N | ✅ | Formato NIE válido |
| `tipoVia` | Rua | ✅ | Tipo de vía válido |
| `nomeVia` | Forno | ✅ | Nombre de vía válido |
| `lugar` | San Cristovo | ✅ | Lugar válido |
| `concello` | Monterrei | ✅ | Concello válido |
| `localidade` | San cristovo (San Cristovo) | ✅ | Localidad válida |
| `cp` | 32618 | ✅ | 5 dígitos |
| `telefonoMovil` | 676920227 | ✅ | 9 dígitos |
| `telefonoMovil_2` | 676920227 | ✅ | 9 dígitos |
| `correo` | joelyshernandezguerrero@gmail.com | ✅ | Contiene @ |
| `correo_2` | joelyshernandezguerrero@gmail.com | ✅ | Contiene @ |
| `dataNacemento` | 24/03/2003 | ✅ | Formato dd/mm/yyyy |
| `tituloEstranxeiro` | Bachiller Tecnico Especialidad Sistemas | ✅ | Texto válido |
| `paisTitulo` | Colombia | ✅ | País válido |
| `nomeCentro` | Institucion Educativa Nuestra Senora de B�len | ✅ | Nombre de centro válido (con error de codificación) |
| `examesOficiais` | Pruebas Saber 11� (ICFES) | ✅ | Texto válido (con error de codificación) |

### Campos que siguen faltando (no detectados)

- `tipoVia_2`
- `nomeVia_2`
- `numero`
- `bloque`
- `andar`
- `porta`
- `parroquia_2`
- `cp_2`
- `provincia_2`
- `concello_2`
- `telefono`
- `telefono_2`

### Campos con valores incoherentes (etiquetas como valor o datos incorrectos)

| Campo | Valor | Motivo |
|---|---|---|
| `parroquia` | OURENSE | OURENSE es una provincia, no una parroquia |
| `nomeRepresentante` | ueipa | Fragmento sin sentido, no un nombre |

### Campos que se mantienen del análisis anterior

| Campo | Antiguo | Nuevo | ¿Mejoró? |
|---|---|---|---|
| `cp` | AYUNTAMIENTO | 32618 | ✅ Sí, de etiqueta a CP válido |
| `nomeRepresentante` | NIF | ueipa | ❌ Sigue siendo incoherente, diferente valor |
| `sexo` | F | F | ✅ Igual, correcto |
| `tipoVia` | NOMBRE DE LA ViA | Rua | ✅ Sí, de etiqueta a tipo de vía válido |
| `tipoVia_2` | NOMBRE DE LA ViA | (no detectado) | ✅ Eliminado el falso positivo |


## Conclusión general

### ¿Ha mejorado el matching?

**SÍ, de forma significativa.**

| Métrica | Antes (antiguo código) | Después (código con variantes en castellano + tolerancia 6x) |
|---|---|---|
| Campos detectados 001 | 6 | 19 |
| Coherentes 001 | 2 (33%) | 16 (84%) |
| Campos detectados 002 | 6 | 24 |
| Coherentes 002 | 2 (33%) | 22 (92%) |
| Falsos positivos (etiquetas como valor) | 9 en total | 5 en total |

### Logros

1. **Eliminación de falsos positivos masivos:** Ya no se detectan etiquetas como `AYUNTAMIENTO`, `NIF`, `NOMBREDE LA VIA` como valores de campo.
2. **Detección de campos críticos:** `cp`, `dni`, `correo`, `tipoVia`, `nome`, `segundoApelido`, `dataNacemento`, `telefonoMovil` ahora se detectan correctamente.
3. **Variantes en castellano funcionan:** `nombre`, `primer apellido`, `fecha de nacimiento`, `ayuntamiento`, `localidad` se reconocen correctamente.
4. **Mayor tolerancia vertical:** Permite encontrar valores que están más abajo de la etiqueta esperada.

### Problemas restantes

1. **`parroquia` detecta "OURENSE" en ambos PDFs:** OURENSE es una provincia, no una parroquia. El algoritmo confunde el nivel territorial.
2. **`nome` detecta "AVENIDA" en 001:** Confunde el tipo de vía con el nombre de la persona.
3. **`lugar` detecta un email en 001:** Asignación incorrecta de campo.
4. **`nomeRepresentante` en 002:** Detecta "ueipa", fragmento sin sentido.
5. **Errores de codificación:** Caracteres como `�` en `nomeCentro` y `examesOficiais` del PDF 002.
6. **Campos aún faltantes:** `telefono`, `numero`, `bloque`, `andar`, `porta`, `provincia_2`, etc. no se detectan de forma consistente.

### Recomendaciones para siguiente sesión

1. Añadir validación de nivel territorial: `parroquia` no debería aceptar nombres de provincia como `OURENSE`.
2. Reforzar la detección de `nome` para que no acepte tipos de vía (`AVENIDA`, `Rua`, `CALLE`, etc.).
3. Revisar el mapeo de `lugar` para evitar asignar direcciones de email.
4. Corregir la lectura de codificación UTF-8 en el OCR de PDFs con caracteres especiales (ñ, á, etc.).
5. Añadir más variantes de etiquetas para `telefono`, `numero`, `bloque`, `andar`, `porta`.

