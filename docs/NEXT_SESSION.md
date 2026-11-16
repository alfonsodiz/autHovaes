# NEXT SESSION

## Objetivo

Escribir ADR-003 (extracción PDF → imagen) y ADR-001 (runtime OCR), y completar `OCR_PIPELINE.md` con los umbrales y la presentación de candidatos.

## Tareas

- [ ] Escribir ADR-003: extracción PDF → imagen (pypdfium2 vs PyMuPDF vs otras).
- [ ] Escribir ADR-001: runtime OCR (PaddleOCR-json, corto porque la decisión está tomada en `OCR_OPTIONS.md`; incluir la decisión sobre el mecanismo de comunicación extensión ↔ proceso Python).
- [ ] Completar `OCR_PIPELINE.md`: umbrales de similitud, N máximo de candidatos, presentación de duplicados.
- [ ] Documentar selectores del formulario ED434A (abrir DevTools, inspeccionar campos). Requiere acceso al formulario autenticado.
- [ ] Definir contrato JSON definitivo con ejemplos completos (`DATA_MODEL.md`).
- [ ] Revisar `DEPLOYMENT_CONSTRAINTS.md` para contradicciones (Native Messaging ↔ registro).

## Resultado esperado

`ADR-003` escrito + `ADR-001` escrito + `OCR_PIPELINE.md` completo + `DEPLOYMENT_CONSTRAINTS.md` coherente. Los selectores del formulario quedan como plantilla pendiente de DevTools.