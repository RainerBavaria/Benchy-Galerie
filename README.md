# Benchy Filament-Galerie

Die Farbübersicht von [Rainer's 3D Stube](https://rainers3dstube.de): Jedes
Filament, das gerade auf Lager ist, wurde als dasselbe kleine Modell gedruckt
und fotografiert — so ist zu sehen, wie eine Farbe wirklich aussieht, statt nur
ihren Namen zu lesen.

Live: <https://rainerbavaria.github.io/Benchy-Galerie/>

## Aufbau

```
index.html       die fertige Seite
filaments.csv    der Bestand, aus dem die Seite ihre Daten liest
images/          die Fotos, ein Bild je Farbe
src/             Quelltext der Seite
tools/           Hilfsskript zum Neubau der index.html
```

Kein Server, keine Datenbank: eine HTML-Datei, eine CSV-Datei, ein Bilderordner.

## Daten

`filaments.csv` wird automatisch aus meiner Filamentverwaltung erzeugt und
hierher übertragen. Angezeigt werden nur Farben, von denen genug Material da
ist; alles andere erscheint gar nicht erst.

Wichtig sind die Spalten `hersteller`, `material`, `farbe`, `hex`, `lagernd`
und `foto`.

## Fotos

JPG im Querformat, Namensschema `MATERIAL_HERSTELLER_FARBE`, zum Beispiel
`PLA-MATTE_SUNLU_WHITE.JPG`. Fehlt ein Bild, zeigt die Karte ein
Platzhalter-Symbol in der hinterlegten Farbe. Endung und Groß-/Kleinschreibung
sind der Seite egal.

## Aussehen ändern

Der Seiteninhalt liegt in `src/gallery-body.html`. Nach einer Änderung dort:

```
python3 tools/build_index.py
```

Das schreibt die `index.html` neu. Die Farben der Oberfläche stehen oben in
`:root` für die helle und in `:root[data-theme="dark"]` für die dunkle
Darstellung.

## Hinweis

Die Fotos zeigen eigene Drucke und dienen als Farbmuster für Auftragsanfragen.
Farben können je nach Bildschirm abweichen.
