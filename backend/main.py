from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import json
import os
import subprocess
from level_up_engine import get_hp_increase

app = FastAPI(title="D&D 2024 VTT API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

CACHE_FILE = "../storage/rules_cache.json"
RULES_DATA = "../data/rules_data.json"
CHAR_ARCHIVE = "../storage/karakterler_arsiv.json"
PHB_REFERENCE = "../reference/phb_2024_referans.md"

class CharacterCreate(BaseModel):
    name: str
    species: str
    char_class: str
    background: str
    level: int
    base_stats: Dict[str, int]
    stat_bonuses: Dict[str, int]
    chosen_skills: List[str]
    languages: str
    alignment: str
    initial_class_choice: Optional[str] = None
    starting_armor: Optional[str] = None
    starting_weapon: Optional[str] = None
    has_shield: bool = False
    chosen_cantrips: Optional[List[str]] = []
    chosen_spells: Optional[List[str]] = []

def load_json(filename):
    if not os.path.exists(filename): return {} if "cache" in filename else []
    with open(filename, 'r', encoding='utf-8') as f:
        try: return json.load(f)
        except: return {} if "cache" in filename else []

def save_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def calculate_modifier(score):
    return (score - 10) // 2

def get_proficiency_bonus(level):
    return 2 + ((level - 1) // 4)

def calculate_ac(char_stats, armor_data, has_shield):
    dex_mod = calculate_modifier(char_stats.get("Dexterity", 10))
    base_ac = 10 + dex_mod
    if armor_data:
        if armor_data["category"] == "Light": base_ac = int(armor_data["ac"].split(' + ')[0]) + dex_mod
        elif armor_data["category"] == "Medium": base_ac = int(armor_data["ac"].split(' + ')[0]) + min(dex_mod, 2)
        elif armor_data["category"] == "Heavy": base_ac = int(armor_data["ac"])
    if has_shield: base_ac += 2
    return base_ac

@app.get("/rules")
def get_rules(): return load_json(RULES_DATA)

@app.get("/characters")
def list_characters(): return load_json(CHAR_ARCHIVE)

@app.get("/character/{name}")
def get_character(name: str):
    archive = load_json(CHAR_ARCHIVE)
    char = next((c for c in archive if c['Isim'].lower() == name.lower()), None)
    if not char: raise HTTPException(status_code=404, detail="Karakter bulunamadı.")
    return char

@app.delete("/character/{name}")
def delete_character(name: str):
    archive = load_json(CHAR_ARCHIVE)
    new_archive = [c for c in archive if c['Isim'].lower() != name.lower()]
    if len(new_archive) == len(archive): raise HTTPException(status_code=404, detail="Silinecek karakter bulunamadı.")
    save_json(CHAR_ARCHIVE, new_archive)
    return {"message": "Karakter silindi."}

@app.post("/character/create")
def create_character(data: CharacterCreate):
    rules = load_json(RULES_DATA)
    c_data = next((item for item in rules['classes'] if item['name'] == data.char_class), None)
    s_data = next((item for item in rules['species'] if item['name'] == data.species), None)
    b_data = next((item for item in rules['backgrounds'] if item['name'] == data.background), None)
    armor_data = next((a for a in rules['armors'] if a['name'] == data.starting_armor), None)
    
    bonuses = data.stat_bonuses
    total_stats = {k: v + bonuses.get(k, 0) for k, v in data.base_stats.items()}
    con_mod = calculate_modifier(total_stats["Constitution"])
    
    hp_die = int(c_data['hit_die'].replace('d', ''))
    total_hp = hp_die + con_mod + ((get_hp_increase(c_data['hit_die']) + con_mod) * (data.level - 1)) if data.level > 1 else hp_die + con_mod

    new_char = {
        "Isim": data.name, "Species": data.species, "Class": data.char_class, "Background": data.background,
        "Level": data.level, "Base_Stats": data.base_stats, "Stat_Bonuslari": bonuses, "HP": total_hp,
        "Armor_Class": calculate_ac(total_stats, armor_data, data.has_shield),
        "Armor_Training": c_data['armor_training'], "Weapon_Proficiency": c_data['weapon_proficiencies'],
        "Proficiency_Bonus": get_proficiency_bonus(data.level), "Languages": data.languages, "Alignment": data.alignment,
        "Origin_Feat": b_data['feat'], "Skills": list(set(b_data['skills'] + data.chosen_skills)),
        "Equipment": { "Armor": data.starting_armor, "Weapon": data.starting_weapon, "Shield": data.has_shield },
        "Spellcasting": { "Cantrips": data.chosen_cantrips, "Spells": data.chosen_spells },
        "Species_Traits": s_data['traits'], "Class_Features": [data.initial_class_choice] if data.initial_class_choice else []
    }
    archive = load_json(CHAR_ARCHIVE)
    # Eğer aynı isimli karakter varsa üzerine yaz (Giriş bilgilerini değiştirme desteği)
    archive = [c for c in archive if c['Isim'].lower() != data.name.lower()]
    archive.append(new_char)
    save_json(CHAR_ARCHIVE, archive)
    return new_char

@app.get("/rule-search")
def search_rule(name: str):
    clean_name = name.split(' (')[0].strip().split(': ')[-1]
    cache = load_json(CACHE_FILE)
    if clean_name in cache: return {"description": cache[clean_name]}
    try:
        prompt = f"PHB 2024 kurallarına göre '{clean_name}' özelliğini kısa ve öz açıkla (Nedir, Mekanik, Sınır). Türkçe ver."
        cmd = f'gemini query "{prompt}" --context {PHB_REFERENCE}'
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', shell=True)
        lines = result.stdout.strip().split('\n')
        cleaned = '\n'.join([l for l in lines if not l.strip().lower().startswith(("i will", "searching", "reading", "checking"))]).strip()
        if cleaned: cache[clean_name] = cleaned; save_json(CACHE_FILE, cache)
        return {"description": cleaned or "Bulunamadı."}
    except: return {"description": "Hata."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
