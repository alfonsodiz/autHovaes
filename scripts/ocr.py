#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Pipeline OCR mínimo.

Fase actual: PDF -> imagen -> OCR (PaddleOCR-json).

Uso:
    python scripts/ocr.py <ruta_al_pdf> [dpi]

Salida:
    - Imprime por stdout un JSON con el contrato de DATA_MODEL.md.
    - Guarda la imagen en recursos/salida/<nombre_pdf>_p1.png
"""

import json
import subprocess
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_LIBS = _HERE.parent / "recursos" / "libs"
if str(_LIBS) not in sys.path:
    sys.path.insert(0, str(_LIBS))

import pypdfium2 as pdfium

_PADDLE_OCR_JSON = _HERE.parent / "recursos" / "paddleocr-json" / "PaddleOCR-json.exe"


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

    pdf = pdfium.PdfDocument(str(pdf_path))
    try:
        if len(pdf) < 1:
            raise ValueError(f"El PDF no tiene páginas: {pdf_path}")

        page = pdf[0]
        scale = dpi / 72.0
        bitmap = page.render(scale=scale)
        pil_image = bitmap.to_pil()
        pil_image.save(str(salida_img), format="PNG")
    finally:
        pdf.close()

    return salida_img


def ejecutar_paddleocr_json(imagen_path: Path) -> list:
    """
    Ejecuta PaddleOCR-json sobre una imagen y devuelve la lista de detecciones.

    Invocación (modo CLI de una sola imagen):
        PaddleOCR-json.exe -image_path="ruta" 

    Salida esperada (objeto JSON):
        {"code": 100, "data": [
            {"text": "...", "score": 0.99, "box": [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]},
            ...
        ]}
    """
    if not _PADDLE_OCR_JSON.is_file():
        raise FileNotFoundError(f"No existe PaddleOCR-json: {_PADDLE_OCR_JSON}")

    resultado = subprocess.run(
        [str(_PADDLE_OCR_JSON), f'-image_path={imagen_path}'],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=str(_PADDLE_OCR_JSON.parent),
        timeout=300,
    )

    if resultado.returncode != 0:
        raise RuntimeError(
            f"PaddleOCR-json falló (código {resultado.returncode}): "
            f"{resultado.stderr.strip()}"
        )

    salida = resultado.stdout.strip()
    if not salida:
        return []

    try:
        datos = json.loads(salida)
    except json.JSONDecodeError:
        inicio = salida.find("{")
        fin = salida.rfind("}")
        if inicio != -1 and fin != -1 and fin > inicio:
            datos = json.loads(salida[inicio : fin + 1])
        else:
            raise

    if isinstance(datos, dict):
        if datos.get("code") != 100:
            raise RuntimeError(
                f"PaddleOCR-json devolvió código {datos.get('code')}: "
                f"{datos.get('msg', 'sin mensaje')}"
            )
        datos = datos.get("data", [])
    elif not isinstance(datos, list):
        datos = []

    detecciones = []
    for item in datos:
        if not isinstance(item, dict):
            continue
        texto = item.get("text", "")
        box = item.get("box", [])
        score = item.get("score", 0.0)
        detecciones.append(
            {
                "raw_text": texto,
                "bbox": box if isinstance(box, list) else [],
                "confidence": float(score) if score else 0.0,
            }
        )

    return detecciones


def main(argv):
    if len(argv) not in (2, 3):
        print("Uso: python scripts/ocr.py <ruta_al_pdf> [dpi]", file=sys.stderr)
        return 1

    pdf_path = Path(argv[1]).resolve()
    dpi = int(argv[2]) if len(argv) == 3 else 300
    salida_dir = _HERE.parent / "recursos" / "salida"

    try:
        img_path = extraer_primera_pagina_como_imagen(pdf_path, salida_dir, dpi)
        detecciones = ejecutar_paddleocr_json(img_path)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2

    fields = {}
    for idx, det in enumerate(detecciones):
        clave = f"campo_{idx:03d}"
        fields[clave] = {
            "value": det["raw_text"] or None,
            "confidence": det["confidence"],
            "bbox": det["bbox"],
            "raw_text": det["raw_text"],
            "status": "review" if det["raw_text"] else "missing",
        }

    salida_json = {
        "version": "1.0",
        "source_pdf": pdf_path.name,
        "pages": 1,
        "fields": fields,
        "matching": {},
    }

    print(json.dumps(salida_json, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))