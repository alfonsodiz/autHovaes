# DATA MODEL

Contrato JSON entre el pipeline OCR y la extensión Chrome.

## Estructura general

    {
      "version": "1.0",
      "source_pdf": "solicitud_001.pdf",
      "pages": 1,
      "fields": { },
      "matching": { }
    }

## `fields`

Un objeto por campo del formulario. Todos nacen en `status: "review"`.

    "dni": {
      "value": "12345678Z",
      "confidence": 0.92,
      "bbox": [120, 340, 280, 365],
      "raw_text": "12345678Z",
      "status": "review"
    }

- `value`: valor propuesto (o `null`).
- `confidence`: 0.0-1.0. Solo informativo para la UI.
- `bbox`: coordenadas del recorte en el PDF.
- `raw_text`: texto OCR sin normalizar.
- `status`: `"review"` (hay valor) o `"missing"` (no detectado).

**No existe `status: "auto"`**. Todo valor requiere revisión del usuario.

## `matching`

Resultado del matching territorial. Cada nivel lleva `codigo` (INE) y `nome` (etiqueta del catálogo).

    "matching": {
      "provincia":  { "codigo": "15", "nome": "Coruña (A)" },
      "concello":   { "codigo": "15001", "nome": "Abegondo" },
      "localidade": { "codigo": "1500101", "nome": "Abegondo (Santaia)" },
      "lugar":      { "codigo": "150010100", "nome": "Abegondo" },
      "match_confidence": 0.88,
      "candidates": [
        { "codigo": "150010100", "nome": "Abegondo", "score": 0.95 },
        { "codigo": "150010101", "nome": "Atrio",    "score": 0.62 }
      ]
    }

### Reglas

1. **Códigos INE, no texto**: cada nivel lleva `codigo` y `nome`.
2. **Provincia derivada**: `provincia.codigo` se deriva de los dos primeros dígitos del concello (`15`, `27`, `32`, `36`). Nunca es `null` si hay concello.
3. **`candidates` solo en el nivel de lugar**: los niveles superiores van a `null` si no hay match aceptado.
4. **Duplicados**: si hay múltiples lugares con el mismo `nome` en la misma localidad, todos van en `candidates` con el mismo score. No se elige automáticamente.
5. **Descatalogados**: el catálogo actual no los contiene. Si en un futuro se añaden, el matching debe excluirlos de `candidates`.
6. **Coherencia por prefijo**: si `concello.codigo` es `15001`, `localidade.codigo` debe empezar por `15001`, y `lugar.codigo` por `1500101`. Si no, es un error del pipeline.

## Reglas generales

- **Ningún valor se presenta como definitivo**. La responsabilidad de revisar es del usuario.
- **La extensión precarga por `codigo`** cuando el formulario lo permite. Si no, por `nome` normalizado.
- **El JSON sale siempre completo**: todos los campos del formulario aparecen en `fields`, aunque sean `status: "missing"`.