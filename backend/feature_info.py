import subprocess
import sys
import os

# Dosya yollarını dinamik hale getirelim
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
PHB_REFERENCE = os.path.join(PROJECT_ROOT, "reference", "phb_2024_referans.md")

def get_feature_details(feature_name):
    """
    PHB 2024 dosyasından CLI ile özellik detaylarını çeker.
    """
    # Seviye bilgisini temizle (Örn: 'Action Surge (Level 2)' -> 'Action Surge')
    clean_name = feature_name.split(' (Level')[0].strip()
    
    prompt = (
        f"PHB 2024 kurallarına göre '{clean_name}' özelliğini kısa ve öz açıkla. "
        "Şu bilgileri içersin: \n"
        "1. Kısaca nedir?\n"
        "2. Mekaniği (Zar, aksiyon tipi vb.)\n"
        "3. Kullanım sınırı (Rest, şarj vb.)\n"
        "Lütfen çok kısa ve net (bullet points) olsun."
    )
    
    try:
        # gemini query komutunu çalıştır (Güvenli liste formatı)
        cmd = ["gemini", "query", prompt, "--context", PHB_REFERENCE]
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode != 0:
            return f"Hata: Kural detayı çekilemedi. ({result.stderr})"
            
        return result.stdout.strip()
    except Exception as e:
        return f"Sistem Hatası: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        feat = " ".join(sys.argv[1:])
        print(f"\n🔍 '{feat}' Araştırılıyor...\n")
        print(get_feature_details(feat))
    else:
        print("Kullanım: python feature_info.py \"Özellik Adı\"")
