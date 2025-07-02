import json
import re

SPECIAL_NAMES = {"L-EGO", "FDE", "ABS", "PA/PET", "CMYK", "RGB", "APFEL", "LDO", "O.D.", "glowEx"}


def replace_glow_luminous_in_right(translation_dict):
    # Mapping: englischer Begriff -> deutsches Zielwort (immer groß)
    replacements = {
        "Glow": "Leuchtend",
        "Luminous": "Strahlend"
    }
    # Regex für alle Flexionen von "leuchtend" und "strahlend"
    leuchtend_regex = re.compile(r"\bleuchtend(e[msr]?|es|en|er)?\b", re.IGNORECASE)
    strahlend_regex = re.compile(r"\bstrahlend(e[msr]?|es|en|er)?\b", re.IGNORECASE)

    adjusted_dict = {}
    for left, right in translation_dict.items():
        new_right = right
        # Glow
        if "Glow" in left:
            # Ersetze alle Varianten von "leuchtend" durch "Leuchtend"
            if leuchtend_regex.search(new_right):
                new_right = leuchtend_regex.sub("Leuchtend", new_right)
            else:
                # Falls nicht vorhanden, Präfix hinzufügen
                new_right = "Leuchtend " + new_right
        # Luminous
        elif "Luminous" in left:
            if strahlend_regex.search(new_right):
                new_right = strahlend_regex.sub("Strahlend", new_right)
            else:
                new_right = "Strahlend " + new_right
        adjusted_dict[left] = new_right
    return adjusted_dict

def adjust_right_side_case(translation_dict):
    adjusted_dict = {}
    for left, right in translation_dict.items():
        left_words = left.split()
        right_words = right.split()
        adjusted_right_words = []
        for i, word in enumerate(right_words):
            if i < len(left_words):
                left_word = left_words[i]
                if left_word[:1].isupper():
                    adjusted_word = word[:1].upper() + word[1:]
                else:
                    adjusted_word = word[:1].lower() + word[1:]
                adjusted_right_words.append(adjusted_word)
            else:
                adjusted_right_words.append(word)
        adjusted_dict[left] = ' '.join(adjusted_right_words)
    return adjusted_dict
    
def capitalize_words_with_whitelist(translation_dict, special_names):
    adjusted_dict = {}
    # Regex für Wortgrenzen, damit auch Bindestrich-Kombinationen erkannt werden
    word_pattern = re.compile(r'\b\w[\w/-]*\b', re.UNICODE)
    for left, right in translation_dict.items():
        def repl(match):
            word = match.group(0)
            # Wenn das Wort in der Whitelist ist, 1:1 übernehmen (case-insensitive Vergleich)
            for special in special_names:
                if word.lower() == special.lower():
                    return special
            # Sonst ersten Buchstaben groß, Rest klein
            return word[:1].upper() + word[1:]
        # Ersetze alle Wörter entsprechend
        new_right = word_pattern.sub(repl, right)
        adjusted_dict[left] = new_right
    return adjusted_dict

def add_prefix_based_on_left_key(translation_dict):
    prefix_map = [
        ("Brightest", "(Brightest) "),
        ("Bright", "(Bright) "),
        ("Light", "(Light) "),
        ("Dark", "(Dark) "),
    ]
    adjusted_dict = {}
    for left, right in translation_dict.items():
        prefix_to_add = ""
        for key_prefix, prefix_value in prefix_map:
            # Prüfe, ob der Key mit diesem Präfix beginnt
            if left.startswith(key_prefix):
                # Bei Bright: Prüfe, ob Brightest schon im Key steht
                if key_prefix == "Bright" and left.startswith("Brightest"):
                    # Kein (Bright) setzen, wenn Brightest schon da ist
                    prefix_to_add = ""
                    break
                # Präfix nur setzen, wenn er noch nicht vorhanden ist
                if not right.startswith(prefix_value):
                    prefix_to_add = prefix_value
                break
        if prefix_to_add:
            adjusted_dict[left] = prefix_to_add + right
        else:
            adjusted_dict[left] = right
    return adjusted_dict

def handle_special_cases(translation_dict):
    # Mapping für Spezialfälle (Key: exakter englischer Begriff, Value: gewünschte deutsche Übersetzung)
    special_cases = {
        "Glow in the Dark": "Im Dunkeln leuchten",
        "Glow In The Dark": "Im Dunkeln leuchten",  # falls Groß-/Kleinschreibung variiert
        "Glow in Dark": "Im Dunkeln leuchten",
        "Glow In Dark": "Im Dunkeln leuchten"
    }
    adjusted_dict = {}
    for left, right in translation_dict.items():
        if left in special_cases:
            adjusted_dict[left] = special_cases[left]
        else:
            adjusted_dict[left] = right
    return adjusted_dict

def join_hell_dunkel_farbe(translation_dict):
    pattern = re.compile(r'\b(Hell|Dunkel)\s+([A-Za-zÄÖÜäöüß]+)', re.UNICODE)
    adjusted_dict = {}
    for left, right in translation_dict.items():
        # Suche nach "Hell <Farbe>" oder "Dunkel <Farbe>" und setze zu "HellFarbe"/"DunkelFarbe"
        def repl(match):
            prefix = match.group(1)
            color = match.group(2)
            # Erster Buchstabe der Farbe immer groß
            return f"{prefix}{color[:1].lower()}{color[1:]}"
        new_right = pattern.sub(repl, right)
        adjusted_dict[left] = new_right
    return adjusted_dict

def replace_luminous_in_key_and_value(translation_dict):
    adjusted_dict = {}
    for left, right in translation_dict.items():
        if re.search(r'\bLuminous\b', left, re.IGNORECASE):
            # Ersetze alle Varianten von "Leuchtend" im Value durch "Strahlend"
            new_right = re.sub(r'\bleuchtend(e[msr]?|es|en|er)?\b', 'Strahlend', right, flags=re.IGNORECASE)
            # Falls "Strahlend" jetzt nicht im Value ist, als Präfix einfügen
            if 'Strahlend' not in new_right:
                new_right = 'Strahlend ' + new_right
            adjusted_dict[left] = new_right
        else:
            adjusted_dict[left] = right
    return adjusted_dict

def main():
    input_file = 'translation_dict_de.json'
    output_file = 'translation_dict_de_corrected.json'
    with open(input_file, 'r', encoding='utf-8') as f:
        translation_dict = json.load(f)
    # 1. Spezialfälle zuerst behandeln
    translation_dict = handle_special_cases(translation_dict)
    # 2. Glow/Luminous etc.
    translation_dict = replace_luminous_in_key_and_value(translation_dict)
    # translation_dict = replace_glow_luminous_in_right(translation_dict)
    # 3. Groß-/Kleinschreibung anpassen
    # translation_dict = adjust_right_side_case(translation_dict)
    # 4. Präfixe ergänzen
    # translation_dict = add_prefix_based_on_left_key(translation_dict)
    translation_dict = join_hell_dunkel_farbe(translation_dict)
    # Alle Anfangsbuchstaben groß
    translation_dict = capitalize_words_with_whitelist(translation_dict, SPECIAL_NAMES)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(translation_dict, f, ensure_ascii=False, indent=2)
    print(f"Angepasste Datei gespeichert als '{output_file}'.")


if __name__ == "__main__":
    main()
