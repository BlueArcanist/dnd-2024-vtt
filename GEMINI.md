# D&D 2024 VTT Proje Protokolü

Bu dosya, projenin mimarisini, kural setlerini ve geliştirme standartlarını tanımlar. Gemini CLI bu projede işlem yaparken bu yönergelere sıkı sıkıya bağlı kalmalıdır.

## 1. Temel Kaynak ve Doğrulama
*   **Ana Referans:** Tüm mekanik kararlar için `phb_2024_referans.md` dosyası tek otoritedir.
*   **Veri Bankaları:** 
    *   `rules_data.json`: Irk, Sınıf ve Geçmişlerin temel verilerini tutar.
    *   `feature_map.json`: Seviye atlama (Level 1-20) tablosunu tutar.
    *   `rules_cache.json`: Canlı kural sorgularının (CLI `gemini query`) sonuçlarını saklar.

## 2. Karakter İnşası Kuralları (PHB 2024)
Her karakter üretimi şu adımları izlemelidir:
*   **Standard Array:** Statlar sadece `15, 14, 13, 12, 10, 8` değerlerinden oluşmalı ve her değer bir kez kullanılmalıdır.
*   **Background Bonus:** Seçilen Background'un sunduğu 3 stat arasından kullanıcı birine +2, diğerine +1 (veya üçüne +1) atamalıdır.
*   **Level 1 Kararları:**
    *   Cleric: Divine Order (Protector/Thaumaturge) seçtirilmeli.
    *   Druid: Primal Order (Magician/Warden) seçtirilmeli.
    *   Fighter: Fighting Style Feat seçtirilmeli.
*   **HP Hesaplama:** 
    *   Lvl 1: Hit Die Max + Con Modifier.
    *   Higher Lvl: Seviye başına (Fixed HP + Con Modifier) eklenmelidir.

## 3. Canlı Kural Sorgulama Standartları
*   Karakter kağıdındaki özelliklere tıklandığında `main.py` üzerinden `gemini query` çalıştırılır.
*   **Temizlik:** AI çıktısındaki "I will search...", "Reading file..." gibi düşünce cümleleri `clean_ai_output` fonksiyonu ile mutlaka temizlenmelidir.
*   **Hız:** Sorgular önce `rules_cache.json` dosyasında aranmalı, yoksa canlı sorgu yapılmalıdır.

## 4. Teknik Mimari
*   **Backend:** FastAPI (`main.py`) kullanılmalıdır.
*   **Frontend:** Vanilla HTML/JS (`index.html`) kullanılmalıdır (Bağımlılığı azaltmak için).
*   **Veritabanı:** Prototip aşamasında `karakterler_arsiv.json` kullanılmalıdır.

## 5. Gelecek Geliştirmeler (Yapılacaklar)
*   [ ] **Ekipman Sistemi:** Silah ve Zırh seçimi, ağırlık takibi.
*   [ ] **Dinamik AC:** Giyilen zırha göre Armor Class hesaplama.
*   [ ] **Zar Motoru:** Stat modlarına tıklandığında 1d20 animasyonu ve sonucu.
*   [ ] **Büyü Sistemi:** Cantrip ve Spell Slot takibi.
*   [ ] **Subclass:** 3. seviyede alt sınıf seçimi.

---
*Not: Bu dosya her oturum başında "Research" fazında okunmalı ve projenin tutarlılığı korunmalıdır.*
