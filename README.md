# Benchy Filament-Galerie


Eine statische Seite, die zu jedem Filament ein gedrucktes Benchy zeigt.
Voreingestellt sind nur die lagernden Filamente sichtbar; ein Schalter blendet
die restlichen dazu. Kein Server, keine Datenbank, keine Build-Kette — eine
HTML-Datei, eine CSV-Datei, ein Bilderordner.

```
index.html          die Galerie (fertig gebaut, nicht bearbeiten)
filaments.csv       dein Bestand — das ist die Datei, die du pflegst
images/             die Benchy-Fotos
src/                Quelltext der Seite (nur wenn du das Aussehen ändern willst)
tools/              Hilfsskripte (Spoolman-Export, Neubau der index.html)
```

## 1. Auf GitHub Pages bringen (einmalig, ca. 5 Minuten, kostenlos)

1. Auf github.com einloggen → **New repository** → Name z. B. `benchy-galerie`,
   Sichtbarkeit **Public** (Pages ist nur bei öffentlichen Repos gratis),
   **Create repository**.
2. Auf der neuen, leeren Repo-Seite: **uploading an existing file** anklicken,
   den kompletten Inhalt dieses Ordners hineinziehen (index.html, filaments.csv,
   images/, src/, tools/, README.md) → **Commit changes**.
3. **Settings → Pages**: unter *Build and deployment* Source = *Deploy from a
   branch*, Branch = `main`, Ordner = `/ (root)` → **Save**.
4. Ein bis zwei Minuten warten. Die Seite liegt dann unter
   `https://<dein-github-name>.github.io/benchy-galerie/`.

Eigene Domain (z. B. `filamente.rainers3dstube.de`) geht auch: unter
Settings → Pages → *Custom domain* eintragen und beim Domain-Hoster einen
CNAME auf `<dein-github-name>.github.io` setzen.

## 2. Bestand pflegen

Alles steckt in `filaments.csv`. Auf github.com die Datei öffnen, Stift-Symbol,
ändern, **Commit changes** — nach etwa einer Minute ist die Galerie aktuell.
Genauso gut geht Excel, LibreOffice oder ein Texteditor (als CSV, UTF-8, speichern).

| Spalte | Bedeutung |
|---|---|
| `id` | eindeutiger Kurzname, am besten gleich der Fotoname ohne Endung |
| `hersteller` | Bambu Lab, Extrudr, … |
| `material` | PLA, PETG, ASA, TPU 95A … (wird automatisch zu Filter-Chips) |
| `farbe` | Anzeigename, z. B. „Bambu Grün" |
| `hex` | Farbcode für Farbfeld, Sortierung und Platzhalter, z. B. `#00AE42` |
| `lagernd` | `ja` / `nein`. Leer gelassen entscheidet die Spalte `spulen` |
| `foto` | Dateiname im Ordner `images/`, z. B. `bambu-pla-basic-schwarz.jpg` |
| `duese_c` | Düsentemperatur in °C |
| `bett_c` | Betttemperatur in °C |
| `spulen` | Anzahl Spulen im Regal |
| `notizen` | frei, erscheint in der Detailansicht und wird durchsucht |

Semikolon statt Komma als Trennzeichen (deutsches Excel) erkennt die Seite von
selbst. Text mit Komma gehört in Anführungszeichen.

## 3. Fotos ergänzen

JPG oder WEBP, Querformat 4:3, etwa 1200 × 900 px, nach `images/` legen und den
Dateinamen in die Spalte `foto` eintragen. Fehlt ein Foto, zeigt die Karte ein
Platzhalter-Boot in der hinterlegten Filamentfarbe — die Galerie sieht also von
Anfang an vollständig aus und du füllst nach und nach auf.

Tipp für gleichmäßige Bilder: immer dieselbe Unterlage, dieselbe Ecke der
Werkstatt, Boot leicht schräg von vorn, Tageslicht ohne direkte Sonne. Zehn
Minuten Aufbau einmalig sparen später jede Nachbearbeitung.

## 4. Später mal Spoolman?

`tools/spoolman_export.py` zieht die Spulen aus einer laufenden Spoolman-Instanz
und schreibt daraus die `filaments.csv`:

```
python3 tools/spoolman_export.py --url http://spoolman.local:7912 --fotos .jpg > filaments.csv
```

Lagernd ist, was nicht archiviert ist und mindestens 50 g Rest hat
(`--min-rest` ändert die Schwelle). Solange du kein Spoolman betreibst,
brauchst du das Skript nicht — die CSV von Hand zu pflegen ist bei
30 bis 50 Filamenten schneller.

## 5. Lokal ansehen

`index.html` doppelklicken zeigt Beispieldaten, weil Browser aus einer lokalen
Datei heraus keine CSV nachladen dürfen. Zwei Wege:

* unten auf **CSV vom Rechner laden** klicken und `filaments.csv` auswählen, oder
* im Ordner `python3 -m http.server 8000` starten und
  `http://localhost:8000` öffnen — das entspricht genau dem späteren Pages-Betrieb.

## 6. Aussehen ändern

Der Seiteninhalt liegt in `src/gallery-body.html`. Nach einer Änderung dort:

```
python3 tools/build_index.py
```

Das schreibt die `index.html` neu. Farben stecken oben in `:root`
(hell) und `:root[data-theme="dark"]` (dunkel).
