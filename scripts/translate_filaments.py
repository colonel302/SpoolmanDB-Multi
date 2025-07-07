import shutil
import os
import json
import hashlib
from deep_translator import GoogleTranslator
import glob

# Konfiguration
LANG = "de"
DICT_DIR = "dict"
DICT_PATH = os.path.join(DICT_DIR, f"translation_dict_{LANG}.json")

def auto_translate(name):
    print(f"Starte Übersetzung für: {name}")
    try:
        if any(term in name for term in ["Bambu", "Arctic", "Candy", "Titan"]):
            return name
        translated = GoogleTranslator(source='en', target=LANG).translate(name)
        return translated
    except Exception as e:
        print(f"Übersetzungsfehler bei '{name}': {str(e)}")
        return name

def translate_name(original_name, dictionary):
    # 1. Wörterbuch-Check (vereinfacht)
    if original_name in dictionary:
        print(f"Nutze Wörterbuch für {original_name}: {dictionary[original_name]}")
        return dictionary[original_name]
    
    # 2. Eigennamen nicht übersetzen + eintragen
    if any(term in original_name for term in ["Bambu", "Arctic", "Candy", "Titan"]):
        print(f"Eigenname erkannt: {original_name} – nicht übersetzt")
        dictionary[original_name] = original_name
        return original_name

    # 3. Spezialbegriffe ersetzen
    name = original_name
    special_terms = {
        "Matt": "Matt",
        "Space": "Weltraum",
        "Silk+": "Silk+",
        "Bright": "(Bright) Hell",
        "Light": "(Light) Hell",
        "Silk": "Silk",
        "Ivory": "Elfenbein",
        "Ash": "Asch",
        "Hot Pink": "Hot Pink",
        "Sky": "Himmel",
        "Apple": "Apfel"
    }
    for en, de in special_terms.items():
        name = name.replace(en, de)
    
    # 4. Auto-Übersetzung
    translated = auto_translate(name)
    dictionary[original_name] = translated
    print(f"Neuer Wörterbucheintrag: {original_name} -> {translated}")
    return translated

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

def process_files():
    source_dir = 'filaments'
    target_dir = 'filaments_de'
    os.makedirs(target_dir, exist_ok=True)
    
    trans_dict = load_dictionary()
    dict_updated = False
    all_files_updated = False  # Neue Flag für globale Aktualisierung
    
    # Prüfe Wörterbuch-Änderungen
    current_dict_hash = get_file_hash(DICT_PATH) if os.path.exists(DICT_PATH) else None
    last_dict_hash = None
    
    # Lade letzten Hash (wenn gespeichert)
    if os.path.exists("last_dict_hash.txt"):
        with open("last_dict_hash.txt", "r") as f:
            last_dict_hash = f.read().strip()
    
    # Wenn Wörterbuch geändert wurde
    if current_dict_hash != last_dict_hash:
        print("Wörterbuch wurde manuell aktualisiert -> erzwinge Neugenerierung aller Dateien")
        all_files_updated = True
        dict_updated = True
        # Lösche alle bisherigen übersetzten Dateien
        for f in glob.glob(os.path.join(target_dir, "*.json")):
            os.remove(f)
    
    # Verarbeite Quelldateien
    for filename in os.listdir(source_dir):
        if not filename.endswith('.json'):
            continue
            
        source_path = os.path.join(source_dir, filename)
        target_path = os.path.join(target_dir, filename)
        
        # Erzwinge Neugenerierung wenn Wörterbuch geändert wurde
        if all_files_updated:
            file_updated = True
        else:
            # Normale Hash-Prüfung
            source_hash = get_file_hash(source_path)
            file_updated = False
            if os.path.exists(target_path):
                target_hash = get_file_hash(target_path)
                if source_hash == target_hash:
                    continue
        
        # Datei übersetzen
        with open(source_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        for filament in data.get('filaments', []):
            for color in filament.get('colors', []):
                original = color['name']
                was_in_dict = original in trans_dict
                translated = translate_name(original, trans_dict)
                color['name'] = translated
                
                if not was_in_dict:
                    dict_updated = True
        
        # Speichere übersetzte Datei
        with open(target_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    # Aktualisiere Wörterbuch und speichere Hash
    if dict_updated or all_files_updated:
        save_dictionary(trans_dict)
        # Speichere aktuellen Wörterbuch-Hash
        current_dict_hash = get_file_hash(DICT_PATH)
        with open("last_dict_hash.txt", "w") as f:
            f.write(current_dict_hash)
    
    return all_files_updated or dict_updated

def copy_json_files_to_en():
    source_dir = 'filaments'
    target_dir = 'filaments_en'
    os.makedirs(target_dir, exist_ok=True)
    for filename in os.listdir(source_dir):
        if filename.endswith('.json'):
            source_path = os.path.join(source_dir, filename)
            target_path = os.path.join(target_dir, filename)
            shutil.copy2(source_path, target_path)
            print(f"Kopiert: {source_path} -> {target_path}")

if __name__ == "__main__":
    copy_json_files_to_en()
    updated = process_files()
    print(f"Übersetzungen durchgeführt: {updated}")
