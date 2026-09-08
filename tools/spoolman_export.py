#!/usr/bin/env python3
"""Erzeugt aus einer laufenden Spoolman-Instanz die filaments.csv der Galerie.

Nur nötig, falls du irgendwann Spoolman einsetzt. Ohne Spoolman pflegst du
die filaments.csv einfach direkt — das Skript ist dann überflüssig.

Aufruf:
    python3 tools/spoolman_export.py --url http://spoolman.local:7912 > filaments.csv

Regel: eine Spule zählt als "lagernd", wenn sie nicht archiviert ist und
mindestens --min-rest Gramm Restfilament hat (Standard 50 g). Mehrere Spulen
derselben Farbe werden zu einer Zeile zusammengefasst, die Anzahl landet in
der Spalte "spulen".

Fotos: Der Dateiname wird aus Hersteller + Material + Farbe gebildet, also
z. B. bambu-lab-pla-basic-schwarz.jpg — so heißt dann auch das Foto im
images/-Ordner. Ein Foto, das noch fehlt, ist kein Problem.
"""
import argparse
import csv
import json
import re
import sys
import urllib.request


def slug(*parts):
    s = " ".join(p for p in parts if p).lower()
    for a, b in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss")):
        s = s.replace(a, b)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "filament"


def fetch(url):
    with urllib.request.urlopen(url, timeout=15) as r:
        return json.load(r)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default="http://localhost:7912", help="Basis-URL von Spoolman")
    ap.add_argument("--min-rest", type=float, default=50.0, help="Gramm Restfilament ab denen eine Spule als lagernd gilt")
    ap.add_argument("--fotos", default="", help="Dateiendung für Fotonamen, z. B. .jpg (leer = keine Fotospalte füllen)")
    args = ap.parse_args()

    spools = fetch(args.url.rstrip("/") + "/api/v1/spool?allow_archived=true")

    rows = {}
    for sp in spools:
        fil = sp.get("filament") or {}
        vendor = (fil.get("vendor") or {}).get("name", "")
        material = fil.get("material", "")
        farbe = fil.get("name") or fil.get("color_hex") or "unbenannt"
        hexcode = fil.get("color_hex") or ""
        if hexcode and not hexcode.startswith("#"):
            hexcode = "#" + hexcode
        key = (vendor, material, farbe, hexcode)

        rest = sp.get("remaining_weight")
        voll = not sp.get("archived") and (rest is None or rest >= args.min_rest)

        r = rows.setdefault(key, {
            "id": slug(vendor, material, farbe),
            "hersteller": vendor,
            "material": material,
            "farbe": farbe,
            "hex": hexcode,
            "lagernd": "nein",
            "foto": "",
            "duese_c": fil.get("settings_extruder_temp") or "",
            "bett_c": fil.get("settings_bed_temp") or "",
            "spulen": 0,
            "notizen": (fil.get("comment") or sp.get("comment") or "").replace("\n", " ").strip(),
        })
        if voll:
            r["lagernd"] = "ja"
            r["spulen"] += 1

    out = csv.writer(sys.stdout, lineterminator="\n")
    cols = ["id", "hersteller", "material", "farbe", "hex", "lagernd",
            "foto", "duese_c", "bett_c", "spulen", "notizen"]
    out.writerow(cols)
    for r in sorted(rows.values(), key=lambda x: (x["hersteller"], x["material"], x["farbe"])):
        if args.fotos:
            r["foto"] = r["id"] + args.fotos
        out.writerow([r[c] for c in cols])


if __name__ == "__main__":
    main()
