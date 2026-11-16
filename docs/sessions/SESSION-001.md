# OCR OPTIONS

## Decisión

**PaddleOCR-json (C++) como único motor OCR.**

Cualquier alternativa que requiera instalación de dependencias pesadas (PyTorch, transformers, paddlepaddle) queda descartada por las restricciones de `DEPLOYMENT_CONSTRAINTS.md`.

Cualquier alternativa basada en LLM local queda descartada por **rendimiento** (decisión del 2026-10-26).

## Candidatos y estado

| Motor | Estado | Motivo |
|---|---|---|
| PaddleOCR-json (C++) | ✅ **Elegido** | Sin instalación, offline, subprocess, modelos con manuscrito |
| PaddleOCR (pip) | ❌ Descartado | Requiere paddlepaddle (~8 GB) |
| EasyOCR | ❌ Descartado | Requiere PyTorch |
| TrOCR | ❌ Descartado | Requiere transformers + PyTorch |
| Florence-2 | ❌ Descartado | Requiere transformers |
| VLM local (Ollama + modelo de visión) | ❌ Descartado | Rendimiento inaceptable (decisión 2026-10-26) |
| Tesseract | ❌ Prohibido | `DEPLOYMENT_CONSTRAINTS.md` |

## Evidencia

Estudio externo sitúa PaddleOCR en manuscrito por debajo del 30% de precisión. Esto justifica el diseño de «pre-relleno asistido con revisión total» (no «OCR automático»).

## Pendiente

- Baseline con PDFs reales (10 PDFs, marcar campos correctos/incorrectos por campo).
- Decidir si la precisión en manuscrito es aceptable para el MVP o si hay que reformular el producto.