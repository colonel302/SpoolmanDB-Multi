import shutil
import os

def copy_filaments_json_to_en():
    source = 'public/filaments.json'
    target = 'public/filaments_en.json'
    if os.path.exists(source):
        shutil.copyfile(source, target)
        print(f"Kopiert {source} zu {target}")
    else:
        print(f"Datei {source} existiert nicht.")

if __name__ == "__main__":
    copy_filaments_json_to_en()
