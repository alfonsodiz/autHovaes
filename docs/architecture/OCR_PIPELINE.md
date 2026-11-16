# OCR PIPELINE

## Checklist general

- [ ] PDF -> Imagen
- [ ] Corrección de inclinación
- [ ] Corrección de perspectiva
- [ ] Recorte
- [ ] OCR
- [ ] Normalización de texto
- [ ] Matching territorial
- [ ] Validación

## Matching territorial (detalle)

El matching se descompone en cuatro niveles. Cada nivel solo se ejecuta si el nivel superior tiene match aceptado.

### 1. Provincia

Se deriva del concello cuando exista. No se busca por OCR directo. Si el OCR detecta un nombre de provincia, se usa solo como pista para ordenar candidatos de concello.

### 2. Concello

Búsqueda por similitud (Levenshtein o similar) contra los 317 concellos. Normalización previa:

- Minúsculas.
- Eliminar tildes.
- Colapsar espacios.
- Quitar paréntesis.

Devolver hasta N candidatos (N a definir, probablemente 3-5).

### 3. Localidad

Búsqueda dentro del concello elegido (936-1.271 localidades). Misma normalización. Devolver hasta N candidatos.

### 4. Lugar

Búsqueda dentro de la localidad elegida (5-20 lugares típicos). Misma normalización. Devolver todos los candidatos que superen el umbral.

### Reglas

- **Validación por prefijo INE**: si `concello.codigo` es `15001`, `localidade.codigo` debe empezar por `15001`, y `lugar.codigo` por `1500101`.
- **Duplicados**: devolver todos, nunca elegir automáticamente. La UI muestra `codigo`.
- **Descatalogados**: el catálogo actual no los contiene.
- **Encoding**: leer el catálogo con UTF-8 explícito.

## Pendiente

- Definir umbral de similitud para candidatos.
- Definir N (número máximo de candidatos por nivel).
- Definir cómo presenta la UI los candidatos duplicados.