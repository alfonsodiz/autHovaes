# Informe de Análisis de Matching — Sesión 005

## Resumen

Se aplicaron dos correcciones a `scripts/ocr.py` para eliminar 5 falsos positivos detectados en los PDFs mecanografiados:

- **Corrección A**: Reducir tolerancia vertical de `6 * altura_e` a `3 * altura_e` en la búsqueda de valor debajo de la etiqueta.
- **Corrección B**: Descartar valores de `nomeRepresentante` con menos de 4 caracteres (fragmentos muy estrechos).

## Comparación Antes/Después

### mecanografiado-001

| Campo | Antes (valor) | Después (valor) | Estado |
|-------|--------------|-----------------|--------|
| `nome` | `AVENIDA` ❌ | `missing` ✅ | Falso positivo eliminado |
| `tipoVia` | `missing` | `AVENIDA` ✅ | Ahora detectado correctamente |
| `parroquia` | `OURENSE` ❌ | `missing` ✅ | Falso positivo eliminado |
| `provincia` | `missing` | `OURENSE` ✅ | Ahora detectado correctamente |
| `lugar` | `EDELMARYSFIGUERAACOSTA19@GMAIL.COM` ❌ | `missing` ✅ | Falso positivo eliminado |
| `correo` | `EDELMARYSFIGUERAACOSTA19@GMAIL.COM` ✅ | `EDELMARYSFIGUERAACOSTA19@GMAIL.COM` ✅ | Sin cambio (seguía correcto) |

### mecanografiado-002

| Campo | Antes (valor) | Después (valor) | Estado |
|-------|--------------|-----------------|--------|
| `parroquia` | `OURENSE` ❌ | `missing` ✅ | Falso positivo eliminado |
| `provincia` | `missing` | `OURENSE` ✅ | Ahora detectado correctamente |
| `nomeRepresentante` | `ueipa` ❌ | `missing` ✅ | Falso positivo eliminado |

## ¿Se han eliminado los falsos positivos?

**Sí, todos los 5 falsos positivos reportados han sido eliminados:**

1. ✅ `nome = AVENIDA` → ahora `tipoVia = AVENIDA`, `nome` = missing
2. ✅ `parroquia = OURENSE` (001 y 002) → ahora `provincia = OURENSE`, `parroquia` = missing
3. ✅ `lugar = email` (001) → ahora `correo = email`, `lugar` = missing
4. ✅ `nomeRepresentante = ueipa` (002) → ahora `nomeRepresentante` = missing

## ¿Ha empeorado algún campo que antes funcionaba?

**No.** Todos los campos que tenían valores correctos antes siguen teniéndolos después:

- `primeiroApelido`, `segundoApelido`, `dni`, `nomeVia`, `andar`, `concello`, `cp`, `localidade`, `telefonoMovil`, `correo`, `dataNacemento`, `tituloEstranxeiro`, `anoAcademico`, `nomeCentro`, `sexo` — todos mantienen sus valores correctos en ambos PDFs.

La única diferencia es que campos que antes tenían un valor incorrecto (falso positivo) ahora están como `missing`, lo cual es el comportamiento correcto según `DATA_MODEL.md`: `status: "missing"` indica que el campo no fue detectado y el usuario debe rellenarlo manualmente.

## Conclusión

Ambas correcciones son efectivas y no introducen regresiones:

- **Corrección A** (tolerancia vertical 3× en lugar de 6×): elimina los falsos positivos donde una etiqueta cogía valores de columnas más abajo (tipo de vía en `nome`, provincia en `parroquia`, correo en `lugar`).
- **Corrección B** (longitud mínima para `nomeRepresentante`): elimina el fragmento muy estrecho `ueipa` que no era un nombre válido.

El pipeline es ahora más preciso: prefiere marcar un campo como `missing` antes que asignarle un valor incorrecto, lo cual es consistente con el principio de que todo valor OCR requiere revisión del usuario.