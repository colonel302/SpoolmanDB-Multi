import os
import json
import hashlib
from deep_translator import GoogleTranslator

# Wörterbuchpfad im Zielordner
DICT_PATH = os.path.join('public', 'translation_dict_de.json')

def load_dictionary():
    if os.path.exists(DICT_PATH):
        with open(DICT_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_dictionary(dictionary):
    os.makedirs(os.path.dirname(DICT_PATH), exist_ok=True)
    with open(DICT_PATH, 'w', encoding='utf-8') as f:
        json.dump(dictionary, f, ensure_ascii=False, indent=2)

def get_file_hash(file_path):
    with open(file_path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def auto_translate(name):
    print(f"Starte Übersetzung für: {name}")
    try:
        if any(term in name for term in ["Bambu", "Arctic", "Candy", "Titan"]):
            return name
        translated = GoogleTranslator(source='en', target='de').translate(name)
        return translated
    except Exception as e:
        print(f"Übersetzungsfehler bei '{name}': {str(e)}")
        return name

def translate_name(name, dictionary):
    if any(term in name for term in ["Bambu", "Arctic", "Candy", "Titan"]):
        return name
    special_terms = {
        "Matt": "Matt",
        "Silk": "Seide",
        "Ivory": "Elfenbein",
        "Ash": "Asch",
        "Sky": "Himmel",
        "Apple": "Apfel"
    }
    for en, de in special_terms.items():
        name = name.replace(en, de)
    if name in dictionary and dictionary[name] != name:
        return dictionary[name]
    translated = auto_translate(name)
    print(f"Übersetze: {name} -> {translated}")
    dictionary[name] = translated
    return translated

def process_files():
    source_dir = 'filaments'
    target_dir = 'public'
    os.makedirs(target_dir, exist_ok=True)

    trans_dict = load_dictionary()
    changed_files = []

    for filename in os.listdir(source_dir):
        if not filename.endswith('.json'):
            continue

        source_path = os.path.join(source_dir, filename)
        # Zielname mit _de-Suffix
        if filename.startswith("materials"):
            target_filename = filename.replace('.json', '_de.json')
        else:
            target_filename = filename.replace('.json', '_de.json')
        target_path = os.path.join(target_dir, target_filename)

        source_hash = get_file_hash(source_path)
        if os.path.exists(target_path):
            target_hash = get_file_hash(target_path)
            if source_hash == target_hash:
                continue

        with open(source_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Übersetze alle Namen in Filamenten und Farben
        if "filaments" in data:
            for filament in data.get('filaments', []):
                if "name" in filament:
                    filament["name"] = translate_name(filament["name"], trans_dict)
                for color in filament.get('colors', []):
                    if "name" in color:
                        original = color['name']
                        translated = translate_name(original, trans_dict)
                        color['name'] = translated
                        if original not in trans_dict:
                            trans_dict[original] = translated
                            changed_files.append(filename)
        # Optional: Auch Materialien übersetzen
        if "materials" in data:
            for material in data.get('materials', []):
                if "material" in material:
                    material["material"] = translate_name(material["material"], trans_dict)

        with open(target_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    if changed_files:
        save_dictionary(trans_dict)

    return changed_files

if __name__ == "__main__":
    updated = process_files()
    print(f"Übersetzte Dateien: {updated}")
