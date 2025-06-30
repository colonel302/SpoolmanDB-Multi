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

def generate_root_index():
    public_dir = Path("public")
    supported_langs = [d.name for d in public_dir.iterdir() if d.is_dir()]
    default_lang = 'en'
    
    # Dynamischer Repository-Name aus GitHub Actions Umgebung
    repo_name = os.environ.get('GITHUB_REPOSITORY', '').split('/')[-1]  # Extrahiert "SpoolmanDB-Multi" aus "user/SpoolmanDB-Multi"
    
    root_index = public_dir / "index.html"
    root_index.write_text(f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Filament Redirect</title>
    <script>
        // Dynamische Weiterleitung mit Repository-Namen
        const userLang = navigator.language.split('-')[0];  // Korrekte Extraktion des Sprachcodes
        const supportedLangs = {supported_langs};
        const defaultLang = '{default_lang}';
        const repoName = '{repo_name}';
        
        if (supportedLangs.includes(userLang)) {{
            window.location.href = `/${{repoName}}/${{userLang}}/index.html`;
        }} else {{
            window.location.href = `/${{repoName}}/${{defaultLang}}/index.html`;
        }}
    </script>
</head>
<body>
    <p>Redirecting to your language...</p>
</body>
</html>''', encoding='utf-8')
    print(f"✅ Root index.html generiert mit Sprachen: {supported_langs} und Repo: {repo_name}")

if __name__ == "__main__":
    generate_html_files()
    generate_root_index()