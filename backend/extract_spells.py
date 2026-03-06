import re
import json

def extract_spells():
    with open('../reference/phb_2024_referans.md', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    spells_data = {
        "Bard": {"Cantrips": [], "Level 1": []},
        "Cleric": {"Cantrips": [], "Level 1": []},
        "Druid": {"Cantrips": [], "Level 1": []},
        "Paladin": {"Level 1": []}, # Paladins get spells at level 1 in 2024
        "Ranger": {"Level 1": []},  # Rangers get spells at level 1 in 2024
        "Sorcerer": {"Cantrips": [], "Level 1": []},
        "Warlock": {"Cantrips": [], "Level 1": []},
        "Wizard": {"Cantrips": [], "Level 1": []}
    }

    current_class = None
    current_level = None

    # Magic words to look for
    headers = {
        "CANTRIPS (LEVEL 0 BARD SPELLS)": ("Bard", "Cantrips"),
        "LEVEL 1 BARD SPELLS": ("Bard", "Level 1"),
        "CANTRIPS (LEVEL 0 CLERIC SPELLS)": ("Cleric", "Cantrips"),
        "LEVEL 1 CLERIC SPELLS": ("Cleric", "Level 1"),
        "CANTRIPS (LEVEL 0 DRUID SPELLS)": ("Druid", "Cantrips"),
        "LEVEL 1 DRUID SPELLS": ("Druid", "Level 1"),
        "LEVEL 1 PALADIN SPELLS": ("Paladin", "Level 1"),
        "LEVEL 1 RANGER SPELLS": ("Ranger", "Level 1"),
        "CANTRIPS (LEVEL 0 SORCERER SPELLS)": ("Sorcerer", "Cantrips"),
        "LEVEL 1 SORCERER SPELLS": ("Sorcerer", "Level 1"),
        "CANTRIPS (LEVEL 0 WARLOCK SPELLS)": ("Warlock", "Cantrips"),
        "LEVEL 1 WARLOCK SPELLS": ("Warlock", "Level 1"),
        "CANTRIPS (LEVEL 0 WIZARD SPELLS)": ("Wizard", "Cantrips"),
        "LEVEL 1 WIZARD SPELLS": ("Wizard", "Level 1")
    }

    # Stop words that mean we reached the next spell level
    stops = ["LEVEL 2", "LEVEL 1", "CANTRIPS", "CHAPTER", "SPELL DESCRIPTIONS", "Spell\n", "School\n", "Special\n", "C\n", "R\n", "M\n", "C, R\n", "R, M\n", "Abjuration\n", "Conjuration\n", "Divination\n", "Enchantment\n", "Evocation\n", "Illusion\n", "Necromancy\n", "Transmutation\n"]
    
    stop_prefixes = ["LEVEL 2 ", "CHAPTER "]

    capture = False

    for line in lines:
        clean_line = line.strip()
        
        # Check if we hit a new section
        found_header = False
        for h, (cls, lvl) in headers.items():
            if h.replace('0', 'O') in clean_line or h in clean_line:
                current_class = cls
                current_level = lvl
                capture = True
                found_header = True
                break
        
        if found_header:
            continue

        if capture:
            # Check for stop conditions
            if any(clean_line.startswith(sp) for sp in stop_prefixes):
                capture = False
                continue
                
            # Skip empty lines, headers, numbers, schools, and special tags
            if not clean_line: continue
            if clean_line in ["Spell", "School", "Special", "C", "R", "M", "C, R", "R, M"]: continue
            if clean_line in ["Abjuration", "Conjuration", "Divination", "Enchantment", "Evocation", "Illusion", "Necromancy", "Transmutation"]: continue
            if clean_line.isdigit(): continue
            if "The following is an ephemeral message" in clean_line: continue
            
            # Additional cleanup for multi-word schools or weird artifacts
            if "table" in clean_line.lower() or "lists" in clean_line.lower(): continue
            
            spells_data[current_class][current_level].append(clean_line)

    with open('../data/spells_data.json', 'w', encoding='utf-8') as f:
        json.dump(spells_data, f, indent=4, ensure_ascii=False)
    
    print("Spells extracted successfully!")

if __name__ == "__main__":
    extract_spells()
