#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Esqueleto mínimo del pipeline OCR.

Fase actual: PDF -> imagen (sin OCR todavía).

Uso:
    python scripts/ocr.py <ruta_al_pdf> [dpi]

Salida:
    - Imprime por stdout la ruta de la imagen generada.
    - Guarda la imagen en recursos/salida/<nombre_pdf>_p1.png
"""

import sys
from pathlib import Path

# Añadir recursos/libs al path para que pypdfium2 se importe desde ahí
_HERE = Path(__file__).resolve().parent
_LIBS = _HERE.parent / "recursos" / "libs"
if str(_LIBS) not in sys.path:
    sys.path.insert(0, str(_LIBS))

import pypdfium2 as pdfium


def extraer_primera_pagina_como_imagen(pdf_path: Path, salida_dir: Path, dpi: int = 300) -> Path:
    """
    Extrae la primera página del PDF y la guarda como PNG.

    Args:
        pdf_path: ruta al PDF de entrada.
        salida_dir: directorio donde guardar la imagen.
        dpi: resolución de rasterizado (300 es un buen valor para OCR).

    Returns:
        ruta a la imagen PNG generada.
    """
    if not pdf_path.is_file():
        raise FileNotFoundError(f"No existe el PDF: {pdf_path}")

    salida_dir.mkdir(parents=True, exist_ok=True)
    salida_img = salida_dir / f"{pdf_path.stem}_p1.png"

    # Abrir el PDF
    pdf = pdfium.PdfDocument(str(pdf_path))
    try:
        if len(pdf) < 1:
            raise ValueError(f"El PDF no tiene páginas: {pdf_path}")

        # Renderizar la primera página
        page = pdf[0]
        # scale = dpi / 72 (pdfium usa 72 puntos por pulgada por defecto)
        scale = dpi / 72.0
        bitmap = page.render(scale=scale)
        pil_image = bitmap.to_pil()
        pil_image.save(str(salida_img), format="PNG")
    finally:
        pdf.close()

    return salida_img


def main(argv):
    if len(argv) not in (2, 3):
        print("Uso: python scripts/ocr.py <ruta_al_pdf> [dpi]", file=sys.stderr)
        return 1

    pdf_path = Path(argv[1]).resolve()
    dpi = int(argv[2]) if len(argv) == 3 else 300
    salida_dir = _HERE.parent / "recursos" / "salida"

    try:
        img_path = extraer_primera_pagina_como_imagen(pdf_path, salida_dir, dpi)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2

    print(str(img_path))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))