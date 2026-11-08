# Geode'a kalıcı Türkçe destek (`tr`) — upstream katkı planı

Hedef: `geode-sdk/geode` deposuna **yerelleştirme altyapısı + Türkçe** ekleyen bir PR.
Kabul edilirse Türkçe, mod kurmadan **tüm Geode kullanıcıları** için çalışır ve bizim
modumuz gereksizleşir (modu yine de "hızlı çözüm" olarak bırakabiliriz).

> ⚠️ Bu bir *plan + taslak*. Geode ekibinin tercih ettiği API şekli farklı olabilir;
> PR açmadan önce **Discord'da `#dev-general` / GitHub issue** üzerinden "localization
> support isteniyor mu, hangi formatı tercih edersiniz (gettext mi JSON mu)" diye sor.
> Bu tek mesaj, PR'ının reddedilme riskini ciddi biçimde düşürür.

---

## 1) Neden şimdi?

- Repoda (main, `v6.0.0-alpha.1`) **hiç** yerelleştirme katmanı yok; tüm UI metinleri
  `loader/src/ui/**` içine gömülü.
- Mod ekosistemi büyük (indekste ~985 mod); QOLMod gibi popüler modlar kendi çeviri
  sistemlerini yazmak zorunda kalmış. Ortak bir API gerçek bir ihtiyaç.
- Geode zaten `geode::utils` altında JSON (`geode-sdk/json`) kullanıyor → altyapı hazır.

## 2) Teknik tasarım (3 dosya + 1 klasör)

### a) `loader/include/Geode/utils/Translations.hpp`
```cpp
#pragma once
#include <string>
#include <unordered_map>

namespace geode::i18n {
    // Geode açılışında çağrılır; translations/<lang>.json dosyalarını yükler.
    void load(std::string const& languageCode);

    // Kayıtlı diller: {"en", "tr", ...}
    std::vector<std::string> availableLanguages();

    // Aktif dili değiştirir ("tr", "en"). Kalıcı hale getirmek için
    // Mod::get()->setSavedValue veya loader ayar dosyası kullanılır.
    void setLanguage(std::string const& languageCode);
    std::string getLanguage();

    // Ana API. Çeviri yoksa key'in kendisini döndürür (İngilizceye düşer).
    std::string tr(std::string const& key);

    // Yer tutucu desteği: tr("mod.install_count", {{"count", "12"}})
    std::string tr(std::string const& key,
                   std::unordered_map<std::string, std::string> const& args);
}
```

### b) `loader/src/utils/Translations.cpp`
- Dosya biçimi: **JSON** (gettext değil) — çünkü Geode zaten JSON'a bağımlı,
  ek kütüphane/bin sorunu yok, katkı verenler için en kolayı.
- Konum: `loader/resources/translations/<lang>.json` (loader paketine gömülür).
- Mod yazarları da aynı API'yi kullanabilsin: `Mod::get()->getResourcesDir() / "translations/tr.json"`
  varsa o da yüklenir (mod çevirisi için büyük kazanç).

Örnek `tr.json` (bizim `ceviri-tablosu.tsv` doğrudan buraya dönüşür):
```json
{
  "ui.install": "Yükle",
  "ui.uninstall": "Kaldır",
  "ui.restart_required": "Yeniden Başlatma Gerekli",
  "mods.safe_mode.desc": "Güvenli Mod etkinleştirildi. Çökmeleri önlemek için hiçbir mod yüklenmeyecek."
}
```

> **Önemli:** gettext/`.po` yerine JSON seçersek `tr.po` dosyamızı da
> `arac/po-olustur.py` ile otomatik JSON'a çevirebiliriz (script hazır, tek fonksiyon).

### c) UI koduna uygulama (mekanik ama geniş iş)
`loader/src/ui/**` içindeki ~250 metin şu şekilde sarılır:
```cpp
// önce
createGeodeButton("Restart Now");
// sonra
createGeodeButton(i18n::tr("ui.restart_now"));
```
**Kolay yol:** metinleri tek seferde değiştirmek yerine, `createGeodeButton`,
`Label::create`, `Popup::create` gibi *merkezî* fonksiyonlara `i18n::tr(...)` çağrısı
eklemek (3–5 dosya, ~40 satır). Böylece PR küçük kalır ve gözden geçirmesi kolaylaşır.

### d) Dil seçimi UI'ı
`ModsLayer` içindeki "Switch Theme" butonunun yanına bir **dil butonu** (`globe.png`)
veya `GeodeUI::openGeodeSettings()` içine bir açılır liste. Geode zaten `SelectList`/`FiltersPopup`
bileşenlerine sahip (bkz. `loader/src/ui/mods/popups/FiltersPopup.cpp`).

## 3) PR'ın parçaları (sırayla gönder)

| # | PR | İçerik | Boyut |
|---|---|---|---|
| 1 | `feat: add i18n API skeleton` | `Translations.hpp/.cpp` + `en.json` (anahtarlar) + test | ~300 satır — gözden geçirmesi kolay |
| 2 | `refactor: use i18n keys in loader UI` | merkezî fonksiyonlarda `tr()` | ~40 satır |
| 3 | `feat: add Turkish translation` | `tr.json` (bizim 259 metin) | 1 dosya |
| 4 | `feat: language selector in mod menu` | ayar UI'ı | ~80 satır |

**Tek dev PR yerine 4 küçük PR** — Geode ekibi böyle daha hızlı kabul ediyor.

## 4) Hazırlık kontrol listesi

- [ ] Discord/issue'da format tercihini sor (gettext mi JSON mu)
- [ ] Repoyu fork et, `loader/resources/translations/` yapısını oluştur
- [ ] `messages.pot` / `tr.po` → JSON dönüştürücüyü yaz (script `arac/po-olustur.py` temel alınabilir)
- [ ] Mevcut Türkçe çevirileri gözden geçir: **mağaza açıklamaları hariç** her metin
- [ ] `en.json` anahtar isimlendirmesi: `alan.ekran.ögе` (ör. `mods.popup.uninstall_confirm`)
- [ ] Test: dili `tr` yapıp tüm popupları aç, taşma/kesme var mı bak
- [ ] Katkı rehberini oku (`CONTRIBUTING.md`), commit mesajlarını onlara uydur
- [ ] PR açıklamasına ekran görüntüsü ekle (Türkçe mod menüsü) — ikna ediciliği yüksek

## 5) PR açıklaması taslağı (İngilizce)

```
Add localization support (i18n) with Turkish as the first non-English language

### Motivation
Geode currently hardcodes all UI strings in C++. Mods like QOLMod had to build
their own translation systems, and non-English users can't use the mod menu in
their language. This PR adds a small i18n layer and ships Turkish.

### What's included
- `geode::i18n::tr()` API (JSON-based, zero new dependencies — reuses geode-sdk/json)
- Translation files at `loader/resources/translations/<lang>.json`
- Per-mod translations supported: `<mod resources>/translations/<lang>.json`
- Fallback to English when a key is missing (never crashes / never shows blank text)
- Turkish translation: 259 strings, complete for the current mod menu
- Language selector in the Geode settings popup

### Notes
- No layout changes; only string lookups were introduced in central helpers
  (`createGeodeButton`, `Label::create`, `Popup::create`).
- Turkish needs Latin Extended-A glyphs (ş, ğ, İ, ı). These render in the
  default Geode font; GD's own bitmap fonts (bigFont.fnt) may fall back —
  a follow-up texture pack can address that separately.

### Screenshots
(Türkçe mod menüsü ekran görüntüsü)
```

## 6) Riskler ve cevapları

| Risk | Cevap |
|---|---|
| "Bu API'yi biz yazacağız, bekle" | Issue'da erken sor; onların tasarımına uy, kod ısrar etme |
| "Tüm metinleri PR'da değiştirmek çok büyük" | Sadece merkezî yardımcı fonksiyonlarda `tr()` kullan (PR #2 ~40 satır) |
| "Çeviriler bakımsız kalır" | `tr.json`'u topluluk PR'larına aç; README'de katkı yönergesi |
| "Türkçe karakterler bozuk görünür" | Ayrı font paketi (bkz. PLAN.md §6②) — PR'ı engellemez |

---

### Bu klasördeki ilgili dosyalar
- `upstream/tr.po` — 259 metinlik gettext dosyası (JSON'a çevrilebilir)
- `upstream/messages.pot` — şablon (yeni metin ekleyenler için)
- `../arac/po-olustur.py` — TSV → PO üretici
- `../ceviriler/ceviri-tablosu.tsv` — tek doğru kaynak (buradan her format üretilir)
