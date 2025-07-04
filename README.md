<!--
Dies ist eine Übersetzung und Erweiterung der Original-README von [donkie](https://github.com/donkie/SpoolmanDB).
Vielen Dank an den Originalautor für die Bereitstellung dieses Projekts!
-->

# SpoolmanDB-Multilanguage

Ein zentraler Ort zur Speicherung von Informationen über 3D-Druck-Filamente und deren Hersteller – jetzt mit Mehrsprachigkeit!

Die Datenbank wird über GitHub Pages bereitgestellt und ist hier einsehbar:  
[https://colonel302.github.io/SpoolmanDB-Multi/](https://colonel302.github.io/SpoolmanDB-Multi/)

Du kannst zu dieser Datenbank beitragen, indem du Dateien hinzufügst/bearbeitest und Pull Requests in diesem Repository einreichst.

---

## **Erweiterungen in diesem Fork (SpoolmanDB-Multi)**

### Mehrsprachigkeit & Automatisierung

- **Mehrsprachige Filamentdaten:**  
  Alle Filament- und Materialnamen werden automatisiert in verschiedene Sprachen übersetzt. Die Sprachdateien befinden sich jeweils in `filaments_<lang>/` (Quellen) und werden als `filaments.json` im jeweiligen Sprachordner unter `/public/<lang>/filaments.json` für die Webseite bereitgestellt.  
  Für Englisch bleibt die Datei `filaments.json` (ohne Sprachsuffix) die Standarddatei.

- **Automatisierter Übersetzungsworkflow:**  
  Ein GitHub Actions Workflow (`translate.yml`) überwacht Änderungen an den Originaldateien in `filaments_*/` und erstellt/aktualisiert die Übersetzungen in den jeweiligen Sprachordnern (z.B. `filaments_de/`, `filaments_fr/` usw.).  
  Das Wörterbuch für Übersetzungen (`translation_dict_<lang>.json`) wird pro Sprache gepflegt und kann manuell ergänzt werden.

- **Kompilierung und Deployment:**  
  Das Skript `scripts/compile_lang.py` sammelt alle Filamentdateien aus den Sprachordnern und erstellt daraus zentrale Dateien wie `public/de/filaments.json`, `public/fr/filaments.json` usw.  
  Die englische Datei wird als `filaments.json` bereitgestellt.  
  **materials.json** wird automatisch in jeden Sprachordner kopiert, sodass alle Sprachseiten unabhängig voneinander funktionieren.

- **Sprachumschaltung & Weiterleitung:**  
  Die Hauptseite (`public/index.html`) erkennt automatisch die Browsersprache und leitet auf die passende Sprachversion weiter (z.B. `/de/`, `/en/`).  
  Ein Sprachumschalter in jeder Sprachseite ermöglicht den manuellen Wechsel.

- **Zentrales CSS:**  
  Das zentrale Stylesheet (`styles.css`) liegt im **Root-Verzeichnis des Repositories** und wird nach jedem Build explizit in das Verzeichnis `public/` kopiert.  
  Alle Sprachseiten binden das CSS über einen absoluten Pfad ein:  
  ```
  <link rel="stylesheet" href="/SpoolmanDB-Multi/styles.css">
  ```
  **Hinweis:** Die Datei darf nicht direkt im Quellordner `public/` liegen, da dieser beim Build gelöscht wird. Sie muss immer aus dem Root nach `public/` kopiert werden.

- **Upstream-Kompatibilität:**  
  Die Originaldateien in `filaments_*/` bleiben unverändert. Änderungen am Original-Repository können problemlos übernommen werden, da alle sprachspezifischen Anpassungen und Workflows getrennt verwaltet werden.

---

## **Datei- und Ordnerstruktur**
```
public/
├── index.html               # Hauptweiterleitung (automatisch generiert)
├── styles.css               # Zentrales CSS für alle Sprachen (nach Build hierher kopiert)
├── materials.json           # Zentrale Materialdaten (wird auch in Sprachordner kopiert)
├── de/
│   ├── index.html           # Deutsch (automatisch generiert)
│   ├── filaments.json
│   └── materials.json
├── en/
│   ├── index.html           # Englisch (automatisch generiert)
│   ├── filaments.json
│   └── materials.json
└── ...                      # Weitere Sprachordner nach gleichem Muster
```

---

## **Workflows & Automatisierung**

### **1. Übersetzungs-Workflow (`.github/workflows/translate.yml`):**
- Wird bei Änderungen an den Quelldateien in `filaments_*/` oder an den Übersetzungswörterbüchern automatisch ausgelöst.
- Übersetzt neue/aktualisierte Filamentnamen und aktualisiert die Sprachdateien.

### **2. Build- und Deploy-Workflow (`.github/workflows/deploy.yml`):**
- Wird bei jedem Push auf `main` oder manuell ausgelöst.
- Führt das Kompilierungsskript aus, das:
    - alle Sprachdateien generiert,
    - materials.json verteilt,
    - index.html für jede Sprache und die Hauptweiterleitung erzeugt,
    - das zentrale CSS aus dem Root nach `/public` kopiert,
    - alles nach `/public` schreibt.
- Deployt den Inhalt von `/public` automatisiert auf GitHub Pages mit den offiziellen Actions:
  - [`actions/upload-pages-artifact`](https://github.com/actions/upload-pages-artifact)
  - [`actions/deploy-pages`](https://github.com/actions/deploy-pages)

---

## **Filamente**

Die Quelldateien befinden sich im Ordner `filaments_<lang>`. Beim Deployment der Datenbank werden diese zu einer einzigen JSON-Datei namens `filaments.json` (für Englisch) bzw. `filaments.json` in jedem Sprachordner zusammengefasst/kompiliert.

**Wichtige Felder der Quelldateien:**
- **name** – Produktname (ggf. mit `{color_name}`-Platzhalter)
- **material** – Materialname (z. B. PLA)
- **density** – Dichte in g/cm³
- **weights** – Array von Objekten mit Gewicht, Spulentyp etc.
- **diameters** – Array von Durchmessern in mm
- **extruder_temp**, **bed_temp** *(optional)* – Temperaturangaben
- **finish**, **multi_color_direction**, **pattern**, **translucent**, **glow** *(optional)*
- **colors** – Array mit Farbnamen und Hex-Codes

## **Materialien**

Alle Materialien findest du in der Datei `materials.json`, die in jedem Sprachordner verfügbar ist.

**Wichtige Felder:**
- **material** – Materialname
- **density** – Dichte in g/cm³
- **extruder_temp** – Extrudertemperatur
- **bed_temp** – Betttemperatur

---

## **Technologien & Tools**

- **Python 3.11+** (für Skripte und Automatisierung)
- **GitHub Actions** (für Übersetzungs- und Build-Workflows)
- **deep-translator, pyyaml** (für Übersetzung und Datenhandling)
- **actions/upload-pages-artifact & actions/deploy-pages** (für Deployment, Stand 2025)
- **check-jsonschema** (für Validierung der Filamentdaten)

---

## **Mitmachen & Beiträge**

- Neue Filamentdaten können als `.json` in den jeweiligen `filaments_<lang>/`-Ordner gelegt werden.
- Übersetzungswörterbücher können im `dict/`-Ordner gepflegt werden.
- Fehler, Featurewünsche oder Fragen bitte als [Issue](https://github.com/colonel302/SpoolmanDB-Multi/issues) einstellen.
- Pull Requests sind willkommen!

---

**Hinweis:**  
Diese README ist eine Übersetzung und Erweiterung der [englischen Originalversion](https://github.com/donkie/SpoolmanDB/blob/main/README.md) von [donkie](https://github.com/donkie).  
Vielen Dank an den Originalautor!

---

---

## Hinweis zur Code-Generierung und Anpassung

> Teile dieses Codes wurden mit Unterstützung von **Perplexity AI** (KI-gestützter Assistent) generiert.  
> Ich, Björn, habe den generierten Code **getestet** und **teilweise an die spezifischen Anforderungen dieses Projekts angepasst**.  
> Bitte beachte, dass trotz sorgfältiger Überprüfung Fehler nicht vollständig ausgeschlossen werden können.  
> Für Rückfragen oder Hinweise zu Verbesserungen stehe ich gerne zur Verfügung!

---
**Änderungen in diesem Fork zuletzt aktualisiert: Juni 2025**