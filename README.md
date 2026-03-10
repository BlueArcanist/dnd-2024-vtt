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

## 🚀 Kurulum ve Çalıştırma

1. Depoyu klonlayın ve klasöre girin.
2. Gerekli kütüphaneleri kurun:
   ```bash
   pip install fastapi uvicorn
   ```

### 🌐 Web Uygulamasını Başlatma (FastAPI)
Frontend arayüzünü kullanmak için backend sunucusunu başlatmanız gerekir:
```bash
cd backend
python main.py
```
Sunucu başladıktan sonra `frontend/index.html` dosyasını tarayıcınızda açarak karakter oluşturmaya başlayabilirsiniz.

### 💻 Terminal Uygulamasını Başlatma (CLI)
Sadece komut satırı üzerinden hızlı karakter oluşturmak için:
```bash
python dnd_app.py
```

## 🔐 Güvenlik ve Yapılandırma Notları
- **Dinamik Yollar:** Uygulama artık dosya yollarını (`data/`, `storage/`, `reference/`) proje kök dizinine göre dinamik olarak çözer. Herhangi bir klasörden güvenle çalıştırılabilir.
- **Güvenli Sorgular:** AI kural sorgulama sistemi (Gemini CLI), Shell Injection saldırılarına karşı korumalı hale getirilmiştir.

## 🗺️ Yol Haritası (Gelecek Geliştirmeler)

- [x] **Subclass Sistemi:** 3. seviyede 2024 kurallarına uygun alt sınıf seçimi.
- [x] **Dinamik AC:** Giyilen zırha göre Armor Class hesaplama.
- [ ] **Weapon Mastery:** Silah özelliklerinin (Nick, Topple vb.) mekanik açıklamaları ve entegrasyonu.
- [ ] **General Feats (Lvl 4+):** Seviye atlama ekranlarında yetenek seçimi.
- [ ] **Kaynak ve Dinlenme:** Short/Long Rest takibi, Hit Dice ve kaynak yenileme.
- [ ] **Zar Motoru:** Stat modlarına tıklandığında 1d20 animasyonu.
- [ ] **Büyü Slotu Sistemi:** Cantrip ve Spell Slot takibi.
- [ ] **Durum Takibi:** Condition etkilerinin (Exhaustion vb.) karakter üzerindeki yansımaları.
- [ ] **Online Altyapı:** Çok oyunculu destek.

## 📄 Lisans

Bu proje kişisel kullanım ve hobi amaçlı geliştirilmiştir. D&D 2024 içerikleri Wizards of the Coast'a aittir.

---
*Bu README dosyası Gemini CLI tarafından otomatik olarak yapılandırılmıştır.*