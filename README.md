# D&D 2024 VTT Projesi 🎲

Bu proje, **Dungeons & Dragons 2024 (PHB 2024)** kurallarını temel alan, modern bir sanal masaüstü (VTT) karakter yönetim ve kural sorgulama sistemidir. FastAPI tabanlı backend ve hafif bir frontend mimarisi ile karakter oluşturma sürecini otomatize eder ve kurallara hızlı erişim sağlar.

## ✨ Temel Özellikler

*   **PHB 2024 Uyumluluğu:** Tüm mekanikler `phb_2024_referans.md` dosyasındaki resmi kurallara göre kurgulanmıştır.
*   **Karakter İnşası:** 
    *   **Standard Array** (15, 14, 13, 12, 10, 8) zorunluluğu.
    *   Arka plan (Background) bonuslarının otomatik uygulanması.
    *   Sınıfa özel Level 1 seçimleri (Cleric: Divine Order, Druid: Primal Order vb.).
*   **Canlı Kural Sorgulama:** Karakter kağıdındaki özelliklere tıklandığında Gemini AI entegrasyonu ile dinamik kural açıklamaları.
*   **Hızlı Performans:** `rules_cache.json` sistemi ile tekrarlanan kural sorgularında anlık yanıt.

## 🛠️ Teknik Mimari

- **Backend:** Python (FastAPI)
- **Frontend:** Vanilla HTML5, CSS3, JavaScript
- **Veri Katmanı:** JSON tabanlı yerel arşivleme (`storage/`) ve kural veritabanı (`data/`)

## 🚀 Kurulum

1. Depoyu klonlayın:
   ```bash
   git clone https://github.com/BlueArcanist/dnd-2024-vtt.git
   cd dnd-2024-vtt
   ```

2. Gerekli kütüphaneleri kurun:
   ```bash
   pip install fastapi uvicorn
   ```

3. Uygulamayı başlatın:
   ```bash
   python dnd_app.py
   ```

## 🗺️ Yol Haritası (Gelecek Geliştirmeler)

- [ ] **Ekipman Sistemi:** Silah/Zırh seçimi ve ağırlık takibi.
- [ ] **Dinamik AC:** Giyilen zırha göre Armor Class hesaplama.
- [ ] **Zar Motoru:** Stat modlarına tıklandığında 1d20 animasyonu.
- [ ] **Büyü Sistemi:** Cantrip ve Spell Slot takibi.
- [ ] **Alt Sınıflar:** 3. seviyede Subclass seçimi desteği.

## 📄 Lisans

Bu proje kişisel kullanım ve hobi amaçlı geliştirilmiştir. D&D 2024 içerikleri Wizards of the Coast'a aittir.

---
*Bu README dosyası Gemini CLI tarafından otomatik olarak yapılandırılmıştır.*