# HOVAES CATALOG ANALYSIS

## Origen

El catálogo original de Hovaes (`catalogo-hovaes-backup.json`) cubría toda España con una estructura anidada de cuatro niveles y entradas `{ value, text }`. Contenía anomalías: descatalogados, duplicados, provincias vacías, nombres inconsistentes.

## Extracto actual

Extracción propia, limitada a Galicia, con estructura mejorada:

- **Ruta**: `.\recursos\catalogo-hovaes-lugares-galicia-completo.json`
- **Encoding**: UTF-8 sin BOM.
- **Vocabulario**: `codigo` / `nome` (en vez de `value` / `text`).
- **Código explícito en concello, localidad y lugar** (no solo en el lugar).
- **Cobertura**: 317 concellos, 3.790 localidades, 34.164 lugares.

## Diferencias con el original

| Aspecto | Original | Extracto |
|---|---|---|
| Cobertura | Toda España (con vacías) | Solo Galicia |
| Código de concello | No explícito | Campo `codigo` |
| Código de localidad | No explícito | Campo `codigo` |
| Vocabulario | `value` / `text` | `codigo` / `nome` |
| Descatalogados | Presentes | Eliminados en la extracción |
| Duplicados | Presentes | Conservados (23 casos, todos por capital/entidad) |
| Anidamiento | Provincia -> Concello -> Parroquia -> lugares | Provincia -> Concello -> {codigo, localidades} -> Localidad -> {codigo, lugares} |

## Decisiones de limpieza

1. **Descatalogados eliminados**: el extractor excluye entradas `(descatalogada)`. Si el catálogo se regenera, mantener esta limpieza.
2. **Duplicados conservados**: son reales (capital vs entidad). El matching devuelve ambos como candidatos.
3. **Provincias de otras CCAA eliminadas**: fuera de alcance.

## Confirmación con el formulario ED434A

El formulario de la sede de la Xunta carga:

- Concellos por `filtroCodProvincia` (2 dígitos).
- Lugares por `filtroCodLocalidade` (7 dígitos).

Esto confirma que el formulario usa los mismos códigos INE que el catálogo. Nuestra arquitectura de matching por niveles ** refleja el formulario.

## Pendiente

- Licencia de uso del catálogo original (no confirmada).
- Actualización periódica: no automatizada; el catálogo es un artefacto versionado.