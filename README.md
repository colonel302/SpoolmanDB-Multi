<!--
Dies ist eine Übersetzung der Original-README von [donkie](https://github.com/donkie/SpoolmanDB).
Vielen Dank an den Originalautor für die Bereitstellung dieses Projekts!
Übersetzt von Perplexity AI für die deutschsprachige Community.
-->

# SpoolmanDB
Ein zentraler Ort zur Speicherung von Informationen über 3D-Druck-Filamente und deren Hersteller.

Die Datenbank wird über GitHub Pages bereitgestellt und ist hier einsehbar: [https://donkie.github.io/SpoolmanDB/](https://donkie.github.io/SpoolmanDB/)

Du kannst zu dieser Datenbank beitragen, indem du Dateien hinzufügst/bearbeitest und Pull Requests in diesem Repository einreichst.

## Filamente
Die Quelldateien befinden sich im Ordner `filaments`. Beim Deployment der Datenbank werden diese zu einer einzigen JSON-Datei namens `filaments.json` zusammengefasst/kompiliert.

Um die notwendige Duplizierung in den Quelldateien zu begrenzen, wird jede Kombination aus Gewicht, Farbe und Durchmesser in der kompilierten JSON dargestellt. Wenn du beispielsweise zwei Durchmesser, zwei Gewichte und zwei Farben angibst, erhältst du acht Kombinationen in der JSON. Es gibt derzeit keine Möglichkeit, bestimmte Kombinationen auszuschließen; entweder akzeptierst du, dass die Datenbank ungültige Einträge enthält, oder du teilst das Filament-Objekt in mehrere auf.

#### Felder der Quelldateien
 * **name** – Der Produktname. Sollte vermutlich den Formatcode `{color_name}` enthalten, um den Farbnamen automatisch einzufügen.
 * **material** – Der Materialname, z. B. PLA.
 * **density** – Die Dichte des Materials in g/cm³.
 * **weights** – Ein Array von Objekten mit den Feldern `weight`, `spool_weight` und `spool_type`. Gib hier mehrere an, wenn der Hersteller das Filament z. B. auf 1-kg- und 5-kg-Spulen verkauft. `spool_weight` ist optional, aber empfohlen. `spool_type` ist optional und kann "plastic", "cardboard" oder "metal" sein.
 * **diameters** – Ein Array von Durchmessern in mm. Gib hier mehrere an, wenn der Hersteller das Filament z. B. in 1,75 mm und 2,85 mm anbietet.
 * **extruder_temp** *(optional)* – Vom Hersteller empfohlene Extrudertemperatur in °C.
 * **bed_temp** *(optional)* – Vom Hersteller empfohlene Betttemperatur in °C.
 * **finish** *(optional)* – Die Oberflächenbeschaffenheit des Filaments, z. B. "matte" oder "glossy". Nur angeben, wenn das Filament speziell dafür ausgelegt ist.
 * **multi_color_direction** *(optional)* – Die Richtung des Mehrfarben-Filaments, z. B. "coaxial" für ein geteiltes/zweifarbiges Filament oder "longitudinal" für ein Filament, das entlang seiner Länge die Farbe wechselt.
 * **pattern** *(optional)* – Strukturmuster, aktuell werden "marble" oder "sparkle" unterstützt. Weitere können bei Bedarf im Schema ergänzt werden.
 * **translucent** *(optional)* – Boolean true/false, ob das Filament zumindest teilweise durchsichtig ist.
 * **glow** *(optional)* – Boolean true/false, ob das Filament einen Nachleuchteffekt hat.
 * **colors** – Ein Array von Objekten mit den Feldern `name` und `hex`. Name sollte der vom Hersteller verwendete Farbname sein. Hex ist der Hex-Code der Farbe und kann bei transparenten Farben auch einen Alpha-Kanal enthalten. Bei Mehrfarben-Filamenten gib stattdessen `hexes` an und eine Liste von Hex-Codes. Du kannst hier auch die Felder `finish`, `multi_color_direction`, `pattern`, `translucent` und `glow` setzen, falls sich diese Eigenschaften für eine bestimmte Farbe unterscheiden.

## Materialien
Alle Materialien findest du in der Datei `materials.json`.

#### Felder der Quelldateien
 * **material** – Der Materialname, z. B. PLA.
 * **density** – Die Dichte des Materials in g/cm³.
 * **extruder_temp** – Allgemeine Extrudertemperatur für dieses Material.
 * **bed_temp** – Allgemeine Betttemperatur für dieses Material.
