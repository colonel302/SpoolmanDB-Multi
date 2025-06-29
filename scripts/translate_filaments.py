import os
import json
import hashlib
from deep_translator import GoogleTranslator
import glob

# Konfiguration
LANG = "de"
DICT_DIR = "dict"
DICT_PATH = os.path.join(DICT_DIR, f"translation_dict_{LANG}.json")

# ... (auto_translate, translate_name, load_dictionary, save_dictionary, get_file_hash bleiben unverändert) ...

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
    if dict_updated:
        save_dictionary(trans_dict)
        # Speichere aktuellen Wörterbuch-Hash
        current_dict_hash = get_file_hash(DICT_PATH)
        with open("last_dict_hash.txt", "w") as f:
            f.write(current_dict_hash)
    
    return all_files_updated or dict_updated

if __name__ == "__main__":
    updated = process_files()
    print(f"Übersetzungen durchgeführt: {updated}")
