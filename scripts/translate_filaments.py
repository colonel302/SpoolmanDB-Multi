import os
import json
import hashlib
from deep_translator import GoogleTranslator

# Konfiguration
LANG = "de"
DICT_DIR = "dict"
DICT_PATH = os.path.join(DICT_DIR, f"translation_dict_{LANG}.json")

# --- auto_translate (UNVERÄNDERT) ---
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

# --- NEUE translate_name FUNKTION ---
def translate_name(original_name, dictionary):
    # 1. Wörterbuch-Check: Sofort zurückgeben, falls vorhanden
    if original_name in dictionary and dictionary[original_name] != original_name:
        return dictionary[original_name]
    
    # 2. Eigennamen nicht übersetzen
    if any(term in original_name for term in ["Bambu", "Arctic", "Candy", "Titan"]):
        return original_name

    # 3. Spezialbegriffe ersetzen (auf Arbeitskopie)
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
        "Sky": "Himmel",
        "Apple": "Apfel"
    }
    for en, de in special_terms.items():
        name = name.replace(en, de)
    
    # 4. Auto-Übersetzung nur für neue Begriffe
    translated = auto_translate(name)
    dictionary[original_name] = translated  # Nur jetzt eintragen
    print(f"Neuer Wörterbucheintrag: {original_name} -> {translated}")
    return translated

# --- REST DES SKRIPTS (UNVERÄNDERT) ---
def load_dictionary():
    if os.path.exists(DICT_PATH):
        with open(DICT_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_dictionary(dictionary):
    os.makedirs(os.path.dirname(DICT_PATH), exist_ok=True)
    with open(DICT_PATH, 'w', encoding='utf-8') as f:
        json.dump(dictionary, f, ensure_ascii=False, indent=2)

def process_files():
    source_dir = 'filaments'
    target_dir = 'filaments_de'
    os.makedirs(target_dir, exist_ok=True)
    
    trans_dict = load_dictionary()
    changed_files = []
    
    for filename in os.listdir(source_dir):
        if not filename.endswith('.json'):
            continue
            
        source_path = os.path.join(source_dir, filename)
        target_path = os.path.join(target_dir, filename)
        
        # ... (Hash-Prüfung und Dateiverarbeitung wie gehabt)
        
        with open(source_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        for filament in data.get('filaments', []):
            for color in filament.get('colors', []):
                original = color['name']
                translated = translate_name(original, trans_dict)  # HIER WIRD DIE NEUE LOGIC GENUTZT
                color['name'] = translated
                
                # Kennzeichnen, wenn neue Übersetzung (für Wörterbuch-Update)
                if original not in trans_dict:
                    changed_files.append(filename)
        
        with open(target_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    if changed_files:
        save_dictionary(trans_dict)
    
    return changed_files

if __name__ == "__main__":
    updated = process_files()
    print(f"Übersetzte Dateien: {updated}")
