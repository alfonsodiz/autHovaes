# CATALOGS

## Fichero

`.\recursos\catalogo-hovaes-lugares-galicia-completo.json`

Encoding: **UTF-8 sin BOM**. Toda lectura debe forzar UTF-8 explícito (ver `AGENTS.md`).

## Estructura

Jerarquía anidada de cuatro niveles:

    Provincia (clave)
      -> Concello (clave)
           -> { codigo, localidades }
                -> Localidad (clave)
                     -> { codigo, lugares: [ { codigo, nome } ] }

Ejemplo real (A Coruña -> Abegondo -> Abegondo (Santaia)):

    {
      "Coruña (A)": {
        "Abegondo": {
          "codigo": "15001",
          "localidades": {
            "Abegondo (Santaia)": {
              "codigo": "1500101",
              "lugares": [
                { "codigo": "150010100", "nome": "Abegondo" },
                { "codigo": "150010101", "nome": "Atrio" }
              ]
            }
          }
        }
      }
    }

## Códigos INE

- **Concello**: 5 dígitos. Ejemplo: `15001`.
- **Localidad** (parroquia en el Nomenclátor): 7 dígitos. Ejemplo: `1500101`.
- **Lugar**: 9 dígitos. Ejemplo: `150010100`.
- **Provincia**: **no almacenada** en el catálogo. Se deriva de los dos primeros dígitos del código de concello:
  - `15` -> Coruña (A)
  - `27` -> Lugo
  - `32` -> Ourense
  - `36` -> Pontevedra

Esta derivación es parte del contrato: el JSON de salida siempre incluye `provincia.codigo`, aunque el catálogo no lo tenga.

## Vocabulario

- **«Localidad»** = nivel de 7 dígitos. Corresponde funcionalmente a **parroquia** en el Nomenclátor. El formulario ED434A llama «localidade» a este nivel (`filtroCodLocalidade`). El proyecto adopta «localidad» como término funcional.
- **«Lugar»** = nivel de 9 dígitos. Entidad de población.

## Cobertura

Verificada contra el Nomenclátor:

| Provincia | Concellos | Localidades | Lugares |
|---|---|---|---|
| Coruña (A) | 95 | 936 | 11.548 |
| Lugo | 67 | 1.271 | 11.097 |
| Ourense | 92 | 917 | 4.615 |
| Pontevedra | 63 | 666 | 6.904 |
| **Total** | **317** | **3.790** | **34.164** |

Solo Galicia. Provincias de otras CCAA no incluidas.

## Anomalías conocidas

### 1. Descatalogados eliminados

El extracto actual **no contiene** entradas `(descatalogada)`. Fueron eliminadas durante la extracción desde el original de Hovaes.

Si el catálogo se regenera en el futuro, el extractor debe mantener esta limpieza, o el matching debe filtrarlas.

### 2. Duplicados de nombre en la misma localidad (23 casos)

En las localidades que tienen un lugar con el mismo nombre que la propia localidad, el catálogo incluye **dos entradas**:

- Una con el nombre de la **parroquia** en MAIÚSCULAS y con paréntesis: `CABANAS (SAN JULIÁN)`, `CERNEDA (SAN SALVADOR)`, `COS (SAN ESTEBAN)`.
- Otra con el nombre del **lugar poblado** en Capitalizado y sin paréntesis: `Cabanas`, `Cerneda`, `Cos`.

Se diferencian por el `codigo` INE (el último dígito suele ser `0` para la parroquia y otro para el lugar) y por el formato del nombre. Ejemplo (Betanzos):

- `{ codigo: "150090000", nome: "BETANZOS" }` (parroquia)
- `{ codigo: "150090001", nome: "Betanzos" }` (lugar)

**Tratamiento**: el matching devuelve **todos** los candidatos, nunca elige automáticamente. La UI debe mostrar el nombre completo tal como está en el catálogo (uno en mayúsculas con paréntesis, otro capitalizado) **y** el código INE como diferencial. No se puede normalizar a mayúsculas/minúsculas antes de mostrar, porque el formato es parte del diferencial.

### 3. Exceso de concellos respecto al INE

Coruña (A) tiene 95 concellos en el catálogo frente a los 93 del INE. Pontevedra tiene 63 frente a 61. El exceso refleja entidades que el INE agrupa en la capital. No afecta al matching: cada concello tiene código único y válido.

## Fuera de alcance

- Provincias de otras CCAA.
- Entradas descatalogadas.
- Actualización automática desde el Nomenclátor (el catálogo es un artefacto versionado).