# CHANGELOG

## Formato

### YYYY-MM-DD

#### Added

#### Changed

#### Fixed

#### Decisions

## Registro

### 2026-10-26

#### Added

- Catálogo territorial `.\recursos\catalogo-hovaes-lugares-galicia-completo.json`.
- ADR-002: matching por niveles con códigos INE.
- `CATALOGS.md`, `DATA_MODEL.md`, `HOVAES_CATALOG_ANALYSIS.md`, `FORM_ANALYSIS.md`.

#### Decisions

- Provincia derivada por prefijo del concello (`15`, `27`, `32`, `36`).
- «Localidade» como término funcional (nivel de 7 dígitos).
- Descatalogados eliminados en la extracción.
- Duplicados (23) devueltos como candidatos múltiples.

### 2026-11-16

#### Added

- `GLOSARIO.md`: referencia cruzada gallego ↔ castellano ↔ identificador técnico.

#### Changed

- Traducción al castellano de los 21 ficheros `.md` de `docs/`.
- Corrección de mojibake en `CATALOGS.md`, `DATA_MODEL.md` y `DEVELOPMENT_ENVIRONMENT.md`.

#### Decisions

- Política de traducción: texto narrativo a castellano; identificadores técnicos, rutas, claves JSON, valores de enum y nombres propios del catálogo sin cambios.
- `concello` se mantiene como galleguismo técnico del dominio (ver `GLOSARIO.md`).
- `localidade` se traduce a «localidad» en el texto; en backticks cuando es identificador.