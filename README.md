<!--
Dies ist eine Übersetzung und Erweiterung der Original-README von [donkie](https://github.com/donkie/SpoolmanDB).
Vielen Dank an den Originalautor für die Bereitstellung dieses Projekts!
-->

# SpoolmanDB-Multilanguage

Ein zentraler Ort zur Speicherung von Informationen über 3D-Druck-Filamente und deren Hersteller – jetzt mit Mehrsprachigkeit!

Die Datenbank wird über GitHub Pages bereitgestellt und ist hier einsehbar:  
[https://colonels302.github.io/SpoolmanDB-Multi/](https://colonel302.github.io/SpoolmanDB-Multi/)

Du kannst zu dieser Datenbank beitragen, indem du Dateien hinzufügst/bearbeitest und Pull Requests in diesem Repository einreichst.

---

## **Erweiterungen in diesem Fork (SpoolmanDB-Multi)**

**Sprachunterstützung und Übersetzungsautomatisierung:**

- **Mehrsprachige Filamentdaten:**  
  Alle Filament- und Materialnamen werden automatisiert in verschiedene Sprachen übersetzt. Die Sprachdateien befinden sich jeweils in `filaments_<lang>/` (Quellen) und werden als `filaments_<lang>.json` im Verzeichnis `/public` für die Webseite bereitgestellt.  
  Für Englisch bleibt die Datei `filaments.json` (ohne Sprachsuffix) die Standarddatei.

- **Automatisierter Übersetzungsworkflow:**  
  Ein GitHub Actions Workflow (`translate.yml`) überwacht Änderungen an den Originaldateien in `filaments/` und erstellt/aktualisiert die Übersetzungen in den jeweiligen Sprachordnern (z.B. `filaments_de/`, `filaments_fr/` usw.).  
  Das Wörterbuch für Übersetzungen (`translation_dict_<lang>.json`) wird pro Sprache gepflegt und kann manuell ergänzt werden.

- **Kompilierung der Sprachdaten:**  
  Das Skript `scripts/compile_lang.py` sammelt alle Filamentdateien aus den Sprachordnern und erstellt daraus zentrale Dateien wie `public/filaments_de.json`, `public/filaments_fr.json` usw.  
  Die englische Datei wird als `filaments.json` bereitgestellt.

- **Sprachumschaltung auf der Webseite:**  
  Die Webseite unterstützt eine Sprachumschaltung (z.B. Deutsch/Englisch/Französisch) und lädt dynamisch die passenden JSON-Dateien (`filaments_de.json`, `filaments_fr.json` usw.) aus dem `/public`-Verzeichnis. Für Englisch wird immer `filaments.json` geladen.

- **Upstream-Kompatibilität:**  
  Die Originaldateien in `filaments/` bleiben unverändert. Änderungen am Original-Repository können problemlos übernommen werden, da alle sprachspezifischen Anpassungen und Workflows getrennt verwaltet werden.

---

## Filamente

Die Quelldateien befinden sich im Ordner `filaments`. Beim Deployment der Datenbank werden diese zu einer einzigen JSON-Datei namens `filaments.json` (für Englisch) bzw. `filaments_<lang>.json` (für andere Sprachen) zusammengefasst/kompiliert.

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

---

**Hinweis:**  
Diese README ist eine Übersetzung und Erweiterung der [englischen Originalversion](https://github.com/donkie/SpoolmanDB/blob/main/README.md) von [donkie](https://github.com/donkie).  
Vielen Dank an den Originalautor!

---

**Änderungen in diesem Fork zuletzt aktualisiert: Juni 2025**
