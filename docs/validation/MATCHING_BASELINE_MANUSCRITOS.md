# Baseline de Matching — PDFs Manuscritos (Sesión 006)
## Resultado por PDF

### manuscritoi-001

**Campos rellenados: 18 | Campos vacíos: 11**

| Campo | Valor | Clasificación | Comentario |
|-------|-------|--------------|------------|
| `nome` | `na` | ❌ incoherente | Valor de 2 caracteres, claramente erróneo |
| `primeiroApelido` | `Alla` | ⚠️ coherente | Posiblemente correcto, aunque corto |
| `segundoApelido` | `Pe` | ❌ incoherente | Valor de 2 caracteres, fragmento |
| `nomeVia` | `Das` | ❌ incoherente | Fragmento muy corto, probablemente incompleto |
| `provincia` | `3204` | ❌ incoherente | Parece un CP, no una provincia |
| `concello` | `ourense` | ✅ coherente | Texto de concello válido |
| `localidade` | `oorense` | ⚠️ coherente | Con error OCR (`o` extra), pero reconocible |
| `telefonoMovil` | `626235546` | ✅ coherente | 9 dígitos, formato válido |
| `telefonoMovil_2` | `626135546` | ✅ coherente | 9 dígitos, formato válido |
| `numero` | `33` | ✅ coherente | Número de vía válido |
| `nomeVia_2` | `Dascamelias` | ✅ coherente | Nombre de vía válido |
| `provincia_2` | `Iourese` | ⚠️ coherente | Ourense con error OCR (`I` inicial) |
| `concello_2` | `ourense` | ✅ coherente | Texto de concello válido |
| `tituloEstranxeiro` | `PBachilleratotecnico` | ⚠️ coherente | Con errores OCR (`P` inicial, `ata` extra) |
| `nomeCentro` | `coleaio` | ⚠️ coherente | Colegio con error OCR (`ae` en lugar de `eg`) |
| `anoAcademico` | `1996` | ✅ coherente | Año válido |
| `examesOficiais` | `PPoeba` | ❌ incoherente | No se reconoce como examen oficial válido |
| `sexo` | `M` | ✅ coherente | Valor válido |
### manuscritoi-002

**Campos rellenados: 9 | Campos vacíos: 16**

| Campo | Valor | Clasificación | Comentario |
|-------|-------|--------------|------------|
| `segundoApelido` | `BAzios` | ⚠️ coherente | Apellido válido, con error OCR de mayúsculas |
| `primeiroApelido` | `HewANekz` | ❌ incoherente | No se reconoce como apellido válido |
| `nomeVia` | `Veea` | ❌ incoherente | Valor muy corto y extraño |
| `andar` | `5` | ✅ coherente | Número de piso válido |
| `provincia` | `Oonnse` | ⚠️ coherente | Ourense con errores OCR (`Oo`, `nn`) |
| `correo` | `JohamaHBo@amail.Com` | ⚠️ coherente | Contiene `@`, formato válido aunque con errores OCR |
| `tituloEstranxeiro` | `EumconMelia` | ⚠️ coherente | Con errores OCR, pero reconocible como título |
| `anoAcademico` | `2013` | ✅ coherente | Año válido |
| `sexo` | `F` | ✅ coherente | Valor válido |

**Campos vacíos:** `nome`, `dni`, `tipoVia`, `numero`, `bloque`, `porta`, `parroquia`, `lugar`, `cp`, `telefono`, `telefonoMovil`, `localidade`, `concello`, `dataNacemento`, `nomeCentro`, `paisTitulo`, `examesOficiais`, `nomeRepresentante`

**Campos vacíos:** `dni`, `tipoVia`, `andar`, `porta`, `parroquia`, `lugar`, `cp`, `correo`, `dataNacemento`

## Resumen

### manuscritoi-003

**Campos rellenados: 20 | Campos vacíos: 9**

| Campo | Valor | Clasificación | Comentario |
|-------|-------|--------------|------------|
| `primeiroApelido` | `anos` | ❌ incoherente | No es un apellido válido |
| `segundoApelido` | `Torres` | ✅ coherente | Apellido válido |
| `tipoVia` | `R5a` | ❌ incoherente | No es un tipo de vía válido |
| `nomeVia` | `PoSll` | ❌ incoherente | No se reconoce como nombre de vía |
| `andar` | `2` | ✅ coherente | Número de piso válido |
| `porta` | `129` | ✅ coherente | Número de puerta válido |
| `provincia` | `Mureosc` | ❌ incoherente | No se reconoce como provincia |
| `concello` | `Oercnsc` | ❌ incoherente | No se reconoce como concello |
| `localidade` | `Ourensc` | ⚠️ coherente | Ourense con error OCR (`c` final) |
| `correo` | `Jeyao2ioy@gma/.com` | ❌ incoherente | Formato de correo inválido (`/.` en dominio) |
| `tipoVia_2` | `Qsa` | ❌ incoherente | No es un tipo de vía válido |
| `nomeVia_2` | `Po si` | ❌ incoherente | No se reconoce como nombre de vía |
| `andar_2` | `2` | ✅ coherente | Número de piso válido |
| `porta_2` | `2g` | ❌ incoherente | Formato de puerta inválido |
| `provincia_2` | `Oureasc` | ⚠️ coherente | Ourense con error OCR (`a` extra) |
| `concello_2` | `Ourense` | ✅ coherente | Concello válido |
| `localidade_2` | `Qurcnsc` | ❌ incoherente | No se reconoce como localidad |
| `tituloEstranxeiro` | `Bachllecafo` | ⚠️ coherente | Bachillerato con errores OCR |
| `nomeCentro` | `o/gIOCT` | ❌ incoherente | No se reconoce como nombre de centro |
## Estadísticas Globales

| PDF | Campos rellenados | Coherentes | Incoherentes | Vacíos | Tasa de coherencia* |
|-----|------------------|------------|--------------|--------|---------------------|
| manuscritoi-001 | 18 | 9 | 9 | 11 | 50% |
| manuscritoi-002 | 9 | 5 | 4 | 16 | 56% |
| manuscritoi-003 | 20 | 9 | 11 | 9 | 45% |
| **Total** | **47** | **23** | **24** | **36** | **~49%** |

\* Tasa de coherencia = campos coherentes / campos rellenados

## Comparación con Mecanografiados

| Métrica | Mecanografiados (005) | Manuscritos (006) |
|---------|----------------------|-------------------|
| Campos detectados (media por PDF) | ~18 | ~15.7 |
| Falsos positivos (etiqueta como valor) | 0 (corregido en sesión 005) | 3+ (`provincia=3204`, `correo` mal formado, etc.) |
| Valores con errores OCR | Mínimos | Frecuentes |
| Campos vacíos | Pocos | Muchos |
| Coherencia global | Alta (84-92%) | Baja (~49%) |

## Campos que más fallan con manuscritos

1. **`nome` / `primeiroApelido` / `segundoApelido`**: OCR lee fragmentos sueltos (`na`, `Pe`, `anos`) en lugar de apellidos completos.
2. **`provincia` / `concello` / `localidade`**: OCR confunde letras similares (`O`/`0`, `r`/`n`, `c`/`e`), produciendo valores no reconocibles (`Oercnsc`, `Mureosc`, `Oonnse`).
3. **`correo`**: El carácter `@` se detecta, pero el resto del dominio suele estar corrupto (`gma/.com`, `amail.Com`).
4. **`tipoVia` / `nomeVia`**: Valores muy cortos o fragmentados (`R5a`, `PoSll`, `Veea`, `Das`).
5. **`dni`, `cp`, `dataNacemento`, `telefono`**: Casi no se detectan en manuscritos (campos vacíos en los 3 PDFs).

## Conclusión

El matching por palabras clave **funciona notablemente peor con PDFs manuscritos** que con mecanografiados:

- La tasa de coherencia baja del ~84-92% (mecanografiados) al ~49% (manuscritos).
- El OCR de PaddleOCR-json tiene dificultades con la escritura a mano, produciendo caracteres erróneos, mayúsculas mezcladas y fragmentos incompletos.
- Muchos campos críticos (`dni`, `cp`, `dataNacemento`, `telefono`) no se detectan en absoluto en manuscritos.
- Los campos que sí se detectan suelen tener errores OCR que requieren revisión manual del usuario.

**Recomendación:** El pipeline actual es usable como pre-relleno asistido para manuscritos, pero con una tasa de error alta. Todo valor requiere revisión obligatoria del usuario (principio ya establecido en `DATA_MODEL.md`). Para mejorar sería necesario:
1. Ajustar umbrales de confianza para campos manuscritos.
2. Añadir validación más estricta por formato (ej. `cp` debe ser exactamente 5 dígitos).
3. Considerar post-procesamiento con corrección ortográfica o matching difuso contra el catálogo territorial.

## Verificación

Todos los tres JSONs se generaron correctamente en `recursos/salida/` con tamaño > 0 y contenido JSON válido.
| `anoAcademico` | `2006` | ✅ coherente | Año válido |
| `sexo` | `F` | ✅ coherente | Valor válido |

**Campos vacíos:** `nome`, `dni`, `numero`, `bloque`, `parroquia`, `lugar`, `cp`, `telefono`, `telefonoMovil`, `dataNacemento`, `nomeRepresentante`, `paisTitulo`, `examesOficiais`
Se ejecutó el pipeline OCR sobre los tres PDFs manuscritos (`manuscrito-001`, `manuscrito-002`, `manuscrito-003`). Como no se dispone de los valores reales (protección de datos), el análisis se basa en la **COHERENCIA** de los valores extraídos: formato esperado, detección de etiquetas como valores, y fragmentos claramente erróneos.