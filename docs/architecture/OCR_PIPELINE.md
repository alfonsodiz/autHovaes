# OCR PIPELINE

## Checklist general

- [ ] PDF -> Imagen (pypdfium2, ver ADR-003)
- [ ] Corrección de inclinación
- [ ] Corrección de perspectiva
- [ ] Recorte
- [ ] OCR (PaddleOCR-json, ver ADR-001 y `OCR_OPTIONS.md`)
- [ ] Normalización de texto
- [ ] Matching territorial
- [ ] Validación

## Matching territorial (detalle)

El matching se descompone en cuatro niveles. Cada nivel solo se ejecuta si el nivel superior tiene match aceptado.

### 1. Provincia

Se deriva del concello cuando exista. No se busca por OCR directo. Si el OCR detecta un nombre de provincia, se usa solo como pista para ordenar candidatos de concello.

### 2. Concello

Búsqueda por similitud (Levenshtein normalizado) contra los 317 concellos. Normalización previa:

- Minúsculas.
- Eliminar tildes.
- Colapsar espacios.
- Quitar paréntesis.

Devolver hasta N candidatos (ver §Umbrales).

### 3. Localidad

Búsqueda dentro del concello elegido (936-1.271 localidades). Misma normalización. Devolver hasta N candidatos.

### 4. Lugar

Búsqueda dentro de la localidad elegida (5-20 lugares típicos). Misma normalización. Devolver todos los candidatos que superen el umbral.

### Reglas

- **Validación por prefijo INE**: si `concello.codigo` es `15001`, `localidade.codigo` debe empezar por `15001`, y `lugar.codigo` por `1500101`.
- **Duplicados**: devolver todos, nunca elegir automáticamente. La UI muestra `codigo` y el nombre completo tal como está en el catálogo (ver §Duplicados).
- **Descatalogados**: el catálogo actual no los contiene.
- **Encoding**: leer el catálogo con UTF-8 explícito.

## Umbrales

Similitud de Levenshtein normalizada (0.0 = totalmente distinto, 1.0 = idéntico), después de la normalización descrita arriba.

| Nivel | Umbral mínimo | N máximo de candidatos | Justificación |
|---|---|---|---|
| Concello | **≥ 0.70** | **5** | Vocabulario cerrado (317). Umbral bajo para no perder el concello correcto por un error OCR moderado. |
| Localidad | **≥ 0.75** | **5** | Vocabulario más específico (936-1.271). Umbral medio. |
| Lugar | **≥ 0.80** | **todos los que superen el umbral** | 5-20 candidatos típicos por localidad. Umbral alto para que la lista sea manejable. |

**Nota**: los umbrales son una propuesta inicial. Se validan con PDFs reales (ver `OCR_VALIDATION.md`). Si la tasa de acierto es baja, se bajan; si hay demasiado ruido, se suben.

## Duplicados

En las localidades que tienen un lugar con el mismo nombre que la propia localidad, el catálogo incluye dos entradas (parroquia vs lugar). Ver `CATALOGS.md` §Duplicados.

**Tratamiento en la UI**:

1. **Filas separadas**. Nunca se agrupan, nunca se elige una automáticamente.
2. **Nombre completo tal como está en el catálogo**: uno en MAYÚSCULAS con paréntesis (parroquia), otro Capitalizado sin paréntesis (lugar).
3. **Código INE visible** en cada fila. Es el diferencial definitivo.
4. **Score visible** (0.0-1.0), calculado por Levenshtein normalizado.

**No se puede normalizar** a mayúsculas/minúsculas antes de mostrar, porque el formato es parte del diferencial. El usuario decide.

## Pendiente

- Validar los umbrales con PDFs reales.
- Confirmar el mapeo `codAnoAcademico` -> año (ver `FORM_ANALYSIS.md` §Pendiente).
- Verificar si hay más duplicados de los 23 identificados, al recorrer el catálogo completo.