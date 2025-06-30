from enum import StrEnum
import json
from pathlib import Path
from typing import Iterator, TypedDict, NotRequired
import os
import sys
import shutil
import datetime

class SpoolType(StrEnum):
    PLASTIC = "plastic"
    CARDBOARD = "cardboard"
    METAL = "metal"

class Finish(StrEnum):
    MATTE = "matte"
    GLOSSY = "glossy"

class MultiColorDirection(StrEnum):
    COAXIAL = "coaxial"
    LONGITUDINAL = "longitudinal"

class Pattern(StrEnum):
    MARBLE = "marble"
    SPARKLE = "sparkle"

class Weight(TypedDict):
    weight: float
    spool_weight: NotRequired[float]
    spool_type: NotRequired[SpoolType | None]

class Color(TypedDict):
    name: str
    hex: NotRequired[str]
    hexes: NotRequired[list[str]]
    finish: NotRequired[Finish | None]
    multi_color_direction: NotRequired[MultiColorDirection | None]
    pattern: NotRequired[Pattern | None]
    translucent: NotRequired[bool]
    glow: NotRequired[bool]

class Filament(TypedDict):
    name: str
    material: str
    density: float
    weights: list[Weight]
    diameters: list[float]
    colors: list[Color]
    extruder_temp: NotRequired[int]
    extruder_temp_range: NotRequired[list[int]]
    bed_temp: NotRequired[int]
    bed_temp_range: NotRequired[list[int]]
    finish: NotRequired[Finish | None]
    multi_color_direction: NotRequired[MultiColorDirection | None]
    pattern: NotRequired[Pattern | None]
    translucent: NotRequired[bool]
    glow: NotRequired[bool]

SPOOL_TYPE_MAP = {
    None: "n",
    SpoolType.PLASTIC: "p",
    SpoolType.CARDBOARD: "c",
    SpoolType.METAL: "m",
}

TRANSLATIONS = {
    "de": {
        "description": "Finden Sie die neuesten Filament- und Materialdaten für den 3D-Druck.",
        "headline": "Ein Repository der neuesten Filament- und Materialdaten für den 3D-Druck.",
        "description_full": "Dieses Projekt ist Open-Source. Fühlen Sie sich frei, einen Pull Request zu erstellen",
        "data_files_header": "Datendateien",
        "materials_link": "MATERIALIEN",
        "filaments_link": "FILAMENTE",
        "materials_count_text": "Es sind {count} Materialien gelistet."
    },
    "en": {
        "description": "Find the latest filament and materials data for 3D printing.",
        "headline": "A repository of the latest filament and materials data for 3D printing.",
        "description_full": "This project is open-source, feel free to create a pull request",
        "data_files_header": "Data files",
        "materials_link": "MATERIALS",
        "filaments_link": "FILAMENTS",
        "materials_count_text": "{count} materials listed."
    }
}

def generate_id(
    *,
    manufacturer: str,
    name: str,
    material: str,
    weight: float,
    diameter: float,
    spool_type: SpoolType | None,
) -> str:
    name = name.encode("ascii", "ignore").decode()
    weight_s = f"{weight:.0f}"
    diameter_s = f"{diameter:.2f}".replace(".", "")
    spooltype_s = SPOOL_TYPE_MAP[spool_type]
    return f"{manufacturer.lower()}_{material.lower()}_{name.lower()}_{weight_s}_{diameter_s}_{spooltype_s}".replace(
        " ", ""
    )

def expand_filament_data(manufacturer: str, data: Filament) -> Iterator[dict]:
    weights = data["weights"]
    diameters = data["diameters"]
    colors = data["colors"]
    for weight in weights:
        for diameter in diameters:
            for color in colors:
                filament = {
                    "manufacturer": manufacturer,
                    "name": data["name"].replace("{color_name}", color["name"]),
                    "material": data["material"],
                    "density": data["density"],
                    "weight": weight["weight"],
                    "diameter": diameter,
                    "color": color["name"],
                    "hex": color.get("hex"),
                    "id": generate_id(
                        manufacturer=manufacturer,
                        name=data["name"].replace("{color_name}", color["name"]),
                        material=data["material"],
                        weight=weight["weight"],
                        diameter=diameter,
                        spool_type=weight.get("spool_type"),
                    ),
                }
                for key in [
                    "spool_weight", "spool_type", "extruder_temp", "extruder_temp_range",
                    "bed_temp", "bed_temp_range", "finish", "multi_color_direction",
                    "pattern", "translucent", "glow"
                ]:
                    if key in data:
                        filament[key] = data[key]
                    if key in color:
                        filament[key] = color[key]
                    if key in weight:
                        filament[key] = weight[key]
                yield filament

def get_filaments_from_data(data: dict) -> Iterator[dict]:
    for filament_data in data["filaments"]:
        yield from expand_filament_data(data["manufacturer"], filament_data)

def load_json(file: Path) -> dict:
    with file.open(encoding="utf-8") as f:
        return json.load(f)

def compile_for_language(lang: str):
    """Kompiliert Filamentdaten für eine bestimmte Sprache"""
    source_dir = Path(f"filaments_{lang}")
    
    # Prüfe ob Verzeichnis existiert
    if not source_dir.exists():
        print(f"⚠️  Warnung: Sprachverzeichnis '{source_dir}' existiert nicht. Überspringe...")
        return
    
    # Prüfe ob Verzeichnis leer ist
    if not any(source_dir.iterdir()):
        print(f"⚠️  Warnung: Sprachverzeichnis '{source_dir}' ist leer. Überspringe...")
        return
    
    print(f"\n=== Verarbeite Sprache: {lang} ===")
    print(f"Quellverzeichnis: {source_dir}")
    
    all_filaments = []
    for file in source_dir.glob("*.json"):
        print(f"  - Verarbeite Datei: {file.name}")
        try:
            data = load_json(file)
            all_filaments.extend(get_filaments_from_data(data))
        except Exception as e:
            print(f"    ❌ Fehler beim Verarbeiten von {file}: {str(e)}")
            continue

    # Prüfe auf leere Daten
    if not all_filaments:
        print(f"⚠️  Warnung: Keine Filamentdaten in {source_dir} gefunden.")
        return

    # IDs auf Eindeutigkeit prüfen
    seen_ids = set()
    duplicates = []
    for f in all_filaments:
        if f["id"] in seen_ids:
            duplicates.append(f["id"])
        else:
            seen_ids.add(f["id"])
    
    if duplicates:
        print("❌ Fehler: Nicht-eindeutige Filament-IDs gefunden:")
        for dup in set(duplicates):
            print(f"  - {dup}")
        raise ValueError(f"Nicht-eindeutige IDs in Sprache '{lang}'")

    # Sortiere Filamente
    all_filaments.sort(key=lambda x: (x["manufacturer"], x["material"], x["name"]))
    
    # Erstelle Sprachverzeichnis in public/
    output_dir = Path("public") / lang
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "filaments.json"
    
    # Schreibe Ausgabedatei
    print(f"✏️  Schreibe {len(all_filaments)} Filamente nach: {output_path}")
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(all_filaments, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Sprache {lang} erfolgreich verarbeitet!")

def copy_materials_files():
    """Kopiert materials.json in jedes Sprachverzeichnis"""
    materials_src = Path("materials.json")
    if not materials_src.exists():
        print("⚠️  materials.json nicht gefunden. Überspringe Kopiervorgang.")
        return
    
    # Finde alle Sprachverzeichnisse in public/
    for lang_dir in Path("public").iterdir():
        if lang_dir.is_dir():
            dest_path = lang_dir / "materials.json"
            shutil.copy(materials_src, dest_path)
            print(f"📋 Kopierte materials.json nach: {dest_path}")

def generate_html_files():
    template_path = Path("templates/template.html")
    template = template_path.read_text(encoding="utf-8")
    current_year = datetime.datetime.now().year
    
    for lang in TRANSLATIONS:
        lang_dir = Path("public") / lang
        lang_dir.mkdir(parents=True, exist_ok=True)
        
        # Ersetze Platzhalter
        html_content = template
        for key, value in TRANSLATIONS[lang].items():
            html_content = html_content.replace(f"{{{{{key}}}}}", value)
        
        html_content = html_content.replace("{{lang}}", lang)
        html_content = html_content.replace("{{current_year}}", str(current_year))
        
        # Schreibe index.html
        (lang_dir / "index.html").write_text(html_content, encoding="utf-8")
        print(f"✅ {lang}/index.html generiert")
        
def copy_materials_to_languages():
    src = Path("public/materials.json")
    for lang_dir in Path("public").iterdir():
        if lang_dir.is_dir():
            dest = lang_dir / "materials.json"
            shutil.copy2(src, dest)
            print(f"✅ materials.json nach {dest} kopiert")

def main():
    # Automatische Spracherkennung
    languages = set()
    for item in os.listdir():
        if os.path.isdir(item) and item.startswith("filaments_"):
            lang = item.replace("filaments_", "", 1)
            if lang:  # Stelle sicher, dass es nicht leer ist
                languages.add(lang)
    
    # Falls keine Sprachen gefunden
    if not languages:
        print("⚠️  Keine Sprachverzeichnisse gefunden. Verwende Standardsprachen.")
        languages = {"de", "en"}  # Fallback
    
    print(f"🔄 Gefundene Sprachen: {', '.join(languages)}")
    
    # Lösche altes public-Verzeichnis
    public_dir = Path("public")
    if public_dir.exists():
        shutil.rmtree(public_dir)
    public_dir.mkdir(exist_ok=True)
    
    # Verarbeite jede Sprache
    for lang in sorted(languages):
        try:
            compile_for_language(lang)
        except Exception as e:
            print(f"❌ Kritischer Fehler in Sprache '{lang}': {str(e)}")
            sys.exit(1)
    
    # Kopiere materials.json in jedes Sprachverzeichnis
    copy_materials_files()
    
    print("\n🎉 Alle Sprachen erfolgreich kompiliert!")
    
    generate_html_files()
    
    copy_materials_to_languages()

if __name__ == "__main__":
    main()
