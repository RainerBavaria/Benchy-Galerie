#!/usr/bin/env python3
"""Baut aus src/gallery-body.html die fertige index.html.

Nur nötig, wenn du den Seiteninhalt in src/ änderst. Für den normalen
Betrieb (Fotos pflegen, filaments.csv pflegen) wird dieses Skript nicht
gebraucht.

    python3 tools/build_index.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
src = (ROOT / "src" / "gallery-body.html").read_text(encoding="utf-8")

marker = "</style>"
cut = src.index(marker) + len(marker)
head, body = src[:cut], src[cut:]

html = (
    "<!doctype html>\n<html lang=\"de\">\n<head>\n"
    "<meta charset=\"utf-8\">\n"
    "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
    "<meta name=\"description\" content=\"Benchy-Galerie der vorrätigen 3D-Druck-Filamente\">\n"
    f"{head}\n</head>\n<body>{body}\n</body>\n</html>\n"
)
(ROOT / "index.html").write_text(html, encoding="utf-8")
print("index.html geschrieben:", len(html), "Zeichen")
