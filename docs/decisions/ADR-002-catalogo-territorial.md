# ADR-002: Catálogo territorial local con matching por niveles

## Estado

Aceptado.

## Contexto

El proyecto necesita resolver cuatro niveles territoriales (provincia, concello, localidad, lugar) a partir de texto OCR manuscrito. El catálogo original de Hovaes (`catalogo-hovaes-backup.json`) cubría toda España pero tenía anomalías: provincias vacías, descatalogados, duplicados, y un vocabulario (`value`/`text`) poco claro.

Además, el formulario ED434A de la sede de la Xunta carga dinámicamente:

- Concellos por `filtroCodProvincia` (2 dígitos INE).
- Lugares por `filtroCodLocalidade` (7 dígitos INE).

Esto confirma que el formulario trabaja con códigos INE, no con texto.

## Alternativas consideradas

### A) Usar el catálogo original tal cual, con matching por texto

Descartada. Las anomalías (descatalogados, duplicados, provincias vacías) hacen el matching frágil. Además, el vocabulario `value`/`text` no es autoexplicativo.

### B) Normalizar el catálogo a una tabla plana con IDs propios

Descartada. El INE ya es un ID estable y universal. Introducir IDs propios añade mantenimiento sin beneficio. Además, rompe la correspondencia con el formulario.

### C) Extraer un catálogo propio de Galicia con códigos INE explícitos en cada nivel y matching por niveles

**Elegida.** El catálogo local (`.\recursos\catalogo-hovaes-lugares-galicia-completo.json`) tiene códigos INE explícitos en concello, localidad y lugar. El matching es por niveles, validando coherencia por prefijo INE. La provincia se deriva por prefijo del concello.

## Decisión

1. **Fuente única**: `.\recursos\catalogo-hovaes-lugares-galicia-completo.json`, UTF-8 sin BOM.
2. **Cobertura**: Galicia completa. 317 concellos, 3.790 localidades, 34.164 lugares.
3. **Vocabulario**: `codigo` (INE) y `nome` (etiqueta). Nivel de 7 dígitos = «localidad» (parroquia en el Nomenclátor).
4. **Provincia derivada**: dos primeros dígitos del concello (`15`, `27`, `32`, `36`).
5. **Matching por niveles**: provincia -> concello -> localidad -> lugar. Validación por prefijo INE.
6. **Duplicados**: devolver todos los candidatos, nunca elegir automáticamente. La UI muestra el código como diferencial.
7. **Descatalogados**: eliminados en la extracción. El matching no los encuentra.

## Consecuencias

### Positivas

- **34.164 lugares** hacen inviable el matching exhaustivo global. El matching por niveles reduce el candidato típico a 5-20 lugares por localidad. Es la única arquitectura viable.
- **Códigos INE** permiten validar coherencia (un lugar de concello X no puede pertenecer a localidad de concello Y).
- **Vocabulario del formulario y del catálogo coinciden**: «localidade» es el término del formulario ED434A.
- **Precarga por código**: la extensión puede inyectar `codigo` en los `select` del formulario, no `nome`. Más robusto.

### Negativas / Riesgos

- **Encoding crítico**: el fichero es UTF-8 sin BOM. En PowerShell 5.1, `Get-Content -Raw` corrompe los nombres con tilde. Toda lectura debe forzar UTF-8 explícito.
- **23 duplicados** de capital/entidad requieren desambiguación por el usuario. La UI debe mostrar el código.
- **Catálogo estático**: no se actualiza automáticamente. Cada actualización requiere regenerar el extracto y versionar.
- **Licencia del original no confirmada**. Riesgo legal abierto.

## Evidencia

- `GET /hovaes/LugarJson-buscarConcellos.action?filtroCodProvincia=15` -> carga concellos de Coruña.
- `GET /hovaes/LugarJson-buscarLugares.action?filtroCodLocalidade=3205401` -> carga lugares de una localidad de Ourense.

Estas llamadas **no se integran en el diseño** (son internas del formulario, pueden cambiar). Se usan solo como evidencia de que el formulario usa códigos INE.

## ADRs relacionados

- ADR-001 (pendiente): runtime del OCR.