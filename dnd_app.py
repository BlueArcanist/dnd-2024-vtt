import json
import os
import sys

# Backend klasörünü path'e ekleyelim ki feature_info import edilebilsin
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, "backend"))

from feature_info import get_feature_details

# Dosya yolları
RULES_FILE = os.path.join(BASE_DIR, "data", "rules_data.json")
ARCHIVE_FILE = os.path.join(BASE_DIR, "storage", "karakterler_arsiv.json")

def load_rules():
    """rules_data.json dosyasını yükler."""
    if not os.path.exists(RULES_FILE):
        print(f"Hata: {RULES_FILE} dosyası bulunamadı!")
        return None
    with open(RULES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_archive():
    """karakterler_arsiv.json dosyasını yükler."""
    if not os.path.exists(ARCHIVE_FILE):
        return []
    with open(ARCHIVE_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_character(character):
    """Karakteri karakterler_arsiv.json dosyasına ekler."""
    archive = load_archive()
    archive.append(character)
    
    if not os.path.exists(os.path.dirname(ARCHIVE_FILE)):
        os.makedirs(os.path.dirname(ARCHIVE_FILE))
        
    with open(ARCHIVE_FILE, 'w', encoding='utf-8') as f:
        json.dump(archive, f, indent=4, ensure_ascii=False)

def get_input(prompt, options):
    """Kullanıcıdan geçerli bir girdi alır."""
    while True:
        val = input(f"{prompt} ({', '.join(options)}): ").strip()
        match = next((o for o in options if o.lower() == val.lower()), None)
        if match:
            return match
        print(f"Geçersiz seçim. Lütfen listeden birini seçin: {', '.join(options)}")

def create_character():
    rules = load_rules()
    if not rules:
        return

    print("\n=== D&D 2024 Karakter Üretici ===")
    
    name = input("Karakter İsmi: ").strip()
    
    species_list = [s['name'] for s in rules['species']]
    selected_species_name = get_input("Species (Irk) Seçin", species_list)
    selected_species = next(s for s in rules['species'] if s['name'] == selected_species_name)
    
    class_list = [c['name'] for c in rules['classes']]
    selected_class_name = get_input("Class (Sınıf) Seçin", class_list)
    selected_class = next(c for c in rules['classes'] if c['name'] == selected_class_name)
    
    bg_list = [b['name'] for b in rules['backgrounds']]
    selected_bg_name = get_input("Background (Geçmiş) Seçin", bg_list)
    selected_bg = next(b for b in rules['backgrounds'] if b['name'] == selected_bg_name)

    print(f"\n{selected_bg_name} Background'u şu statları destekliyor: {', '.join(selected_bg['ability_scores'])}")
    print("Seçenekler: 1. (+2, +1) | 2. (+1, +1, +1)")
    choice = input("Seçiminiz (1/2): ").strip()
    stat_bonuses = {}
    
    if choice == '1':
        plus2 = get_input("+2 bonus alacak stat", selected_bg['ability_scores'])
        remaining = [s for s in selected_bg['ability_scores'] if s != plus2]
        plus1 = get_input("+1 bonus alacak stat", remaining)
        stat_bonuses = {plus2: 2, plus1: 1}
    else:
        for s in selected_bg['ability_scores']:
            stat_bonuses[s] = 1

    character = {
        "Isim": name,
        "Species": selected_species['name'],
        "Class": selected_class['name'],
        "Background": selected_bg['name'],
        "Level": 1,
        "Stat_Bonuslari": stat_bonuses,
        "Origin_Feat": selected_bg['feat'],
        "Skills": selected_bg['skills'],
        "Tools": selected_bg['tool'],
        "Hit_Die": selected_class['hit_die'],
        "HP": int(selected_class['hit_die'].replace('d', '')),
        "Saving_Throws": selected_class['saving_throws'],
        "Armor_Proficiency": selected_class['armor_training'],
        "Weapon_Proficiency": selected_class['weapon_proficiencies'],
        "Species_Traits": selected_species['traits'],
        "Speed": selected_species['speed'],
        "Size": selected_species['size'],
        "Class_Features": [] # Başlangıçta boş
    }

    print("\n" + "="*40)
    print(f"KARAKTER KAĞIDI: {character['Isim']} (Kaydedildi)")
    print("="*40)
    save_character(character)

def check_feature_info():
    archive = load_archive()
    if not archive:
        print("Arşivde karakter bulunamadı.")
        return

    char_names = [c['Isim'] for c in archive]
    name = get_input("Hangi karakterin özelliklerini incelemek istersiniz?", char_names)
    char = next(c for c in archive if c['Isim'] == name)

    if 'Class_Features' not in char or not char['Class_Features']:
        print(f"{name} için henüz özel bir sınıf yeteneği (level-up ile gelen) yok.")
        return

    print(f"\n--- {name} Yetenekleri ---")
    for i, feat in enumerate(char['Class_Features'], 1):
        print(f"{i}. {feat}")
    
    choice = input("\nAçıklamasını görmek istediğiniz yetenek numarası (veya çıkış için 0): ").strip()
    if choice.isdigit() and 0 < int(choice) <= len(char['Class_Features']):
        feat_name = char['Class_Features'][int(choice)-1]
        print(f"\n🔍 {feat_name} Araştırılıyor (Canlı PHB Sorgusu)...\n")
        details = get_feature_details(feat_name)
        print(details)
    elif choice == '0':
        return
    else:
        print("Geçersiz seçim.")

def main_menu():
    while True:
        print("\n=== D&D VTT PROJESİ ===")
        print("1. Yeni Karakter Üret")
        print("2. Arşivden Yetenek Sorgula (Live PHB)")
        print("3. Çıkış")
        
        choice = input("Seçiminiz: ").strip()
        if choice == '1':
            create_character()
        elif choice == '2':
            check_feature_info()
        elif choice == '3':
            break
        else:
            print("Geçersiz seçim.")

if __name__ == "__main__":
    main_menu()

