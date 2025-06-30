# scripts/translate_html.py
import datetime
from pathlib import Path

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
            placeholder = f"{{{{{key}}}}}"
            html_content = html_content.replace(placeholder, value)
        
        html_content = html_content.replace("{{current_year}}", str(current_year))
        
        # Schreibe index.html
        (lang_dir / "index.html").write_text(html_content, encoding="utf-8")
        print(f"✅ {lang}/index.html generiert")

if __name__ == "__main__":
    generate_html_files()
