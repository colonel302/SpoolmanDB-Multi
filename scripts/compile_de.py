from enum import StrEnum
import json
from pathlib import Path
from typing import Iterator, TypedDict, NotRequired

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
    # Diese Funktion ist identisch zum Original! (Hier als Platzhalter, bitte ggf. die Originalfunktion einfügen)
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
                # Optional: Weitere Felder übernehmen, falls vorhanden
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

def compile_filaments_de():
    """Kompiliert alle deutschen Filamentdaten aus filaments_de/*.json zu public/filaments_de.json"""
    all_filaments = []
    for file in Path("filaments_de").glob("*.json"):
        print(f"Compiling {file}")
        all_filaments.extend(get_filaments_from_data(load_json(file)))

    # IDs prüfen
    seen_ids = set()
    duplicates = [
        f for f in all_filaments if f["id"] in seen_ids or seen_ids.add(f["id"])
    ]
    if duplicates:
        print("ERROR: Non-unique filament IDs found:")
        for f in duplicates:
            print(f["id"])
        raise ValueError("Found non-unique ids")

    all_filaments.sort(key=lambda x: (x["manufacturer"], x["material"], x["name"]))

    output_dir = Path("public")
    output_dir.mkdir(exist_ok=True)
    output_path = Path(f"filaments_{lang}.json")  # z.B. filaments_de.json

    print(f"Writing all filaments to '{output_path}'")
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(all_filaments, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    print("Compiling all german filaments...")
    compile_filaments_de()
    print("Done!")
