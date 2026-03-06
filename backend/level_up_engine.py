import json
import os
import sys

def load_data(file_path):
    if not os.path.exists(file_path):
        return {}
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_data(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def get_hp_increase(hit_die):
    # Fixed HP values per PHB 2024
    mapping = {
        "d12": 7,
        "d10": 6,
        "d8": 5,
        "d6": 4
    }
    return mapping.get(hit_die, 0)

def level_up(character_name, target_level):
    archive_file = 'karakterler_arsiv.json'
    features_file = 'feature_map.json'
    
    archive = load_data(archive_file)
    features_map = load_data(features_file)
    
    if not archive or not features_map:
        print("Hata: Arşiv veya özellik haritası yüklenemedi.")
        return

    char = next((c for c in archive if c['Isim'] == character_name), None)
    
    if not char:
        print(f"Hata: '{character_name}' isimli karakter bulunamadı.")
        return

    current_level = char.get('Level', 1)
    if current_level >= target_level:
        print(f"Bilgi: {character_name} zaten {current_level}. seviyede veya daha yüksek.")
        return

    char_class = char['Class']
    if char_class not in features_map:
        print(f"Hata: {char_class} sınıfı özellik haritasında bulunamadı.")
        return

    # Con Mod hesaplama (Stat_Bonuslari'ndan Con varsa +2/+1 eklenmiş olabilir)
    # Varsayılan Con skoru 10 (+0 mod) kabul edilirse sadece bonuslara bakılır.
    # Ancak basitlik için PHB 2024 Fixed HP (X + Con mod) kuralını Con=10 varsayarak uyguluyoruz.
    con_bonus = char.get('Stat_Bonuslari', {}).get('Constitution', 0)
    # D&D 5e/2024: (Score - 10) // 2. Skor bilinmediği için sadece bonusu (2 veya 1) ekliyoruz.
    con_mod = con_bonus // 2 

    hp_increase_per_level = get_hp_increase(char['Hit_Die']) + con_mod

    # Seviye atlama döngüsü
    for lvl in range(current_level + 1, target_level + 1):
        # HP Güncelleme
        if 'HP' in char:
            char['HP'] += hp_increase_per_level
        elif 'HP_Level_1' in char:
            char['HP'] = char['HP_Level_1'] + hp_increase_per_level
            del char['HP_Level_1']
        
        # Özellikleri ekle
        new_features = features_map[char_class].get(str(lvl), [])
        if 'Class_Features' not in char:
            char['Class_Features'] = []
        
        for feat in new_features:
            feat_entry = f"{feat} (Level {lvl})"
            if feat_entry not in char['Class_Features']:
                char['Class_Features'].append(feat_entry)

    char['Level'] = target_level
    
    save_data(archive_file, archive)
    print(f"Başarı: {character_name} {target_level}. seviyeye yükseltildi! Yeni HP: {char.get('HP', char.get('HP_Level_1'))}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Kullanım: python level_up_engine.py \"Karakter Adı\" HedefSeviye")
    else:
        name = sys.argv[1]
        try:
            target = int(sys.argv[2])
            level_up(name, target)
        except ValueError:
            print("Hata: Seviye bir tam sayı olmalıdır.")
