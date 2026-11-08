# Logo & oyun içi görsel değişimi — Türk temalı paket rehberi

Hedef: GD'nin **logosu**, **menü görselleri** ve **oyun içi arayüz** parçalarını Türk temalı
hale getirmek. Hepsi **Texture Loader** paketiyle yapılır → orijinal `Resources` klasörüne
hiç dokunulmaz, kaldırmak tek tık.

---

## 1) Önce şu kuralı bil (en sık yapılan hata)

GD'de bazı görseller **tek PNG değil, spritesheet içinde** durur. Örneğin ana menüdeki
"Geometry Dash" logosu:

| Görsel | Nerede | Dosya adı |
|---|---|---|
| Ana logo | `GJ_LaunchSheet-hd.plist` içinde `GJ_logo_001.png` karesi | `GJ_LaunchSheet-hd.png` + `.plist` |
| GD Lite / Meltdown / SubZero / World logoları | aynı sheet | `GJ_lite_001.png`, `GJ_md_001.png`, `gj_subzeroLogo_001.png`, `gj_worldLogo_001.png` |
| RobTop logosu | aynı sheet | `RobTopLogoBig_001.png` (1650×973) |
| Butonlar (geri, kapat, sil, ayar, …) | `GJ_GameSheet03-*.plist` (612 kare!) | `GJ_backBtn_001.png`, `GJ_closeBtn_001.png`, `GJ_deleteBtn_001.png`, `GJ_achBtn_001.png`, … |
| Arka plan gradyanı | tek PNG | `GJ_gradientBG-hd.png` / `-uhd.png` |
| Buton zemini | tek PNG | `GJ_button_01..06-hd/uhd.png`, `GJ_square01..05` |
| Fontlar | `.fnt` + `_0.png` | `bigFont`, `goldFont` (bkz. FONT-NOTLARI.md) |

**Sonuç:** `GJ_logo_001.png` adında bir dosya koymak işe yaramaz. Doğru yol:
`GJ_LaunchSheet-hd.png` + `GJ_LaunchSheet-hd.plist` ikilisini paketlemek ve plist içinde
o karenin koordinatlarını kendi logona göre güncellemek.

## 2) Hazır şablon: logonun tam boyutu

Orijinal logoyu plist'ten çıkardım — **tam bu ölçülerde** tasarla, yoksa oyunda esner/bozulur:

| Dosya | Boyut (px) |
|---|---|
| `sablon/GJ_logo_001-hd-sablon.png` | **843 × 102** |
| `sablon/GJ_logo_001-uhd-sablon.png` | **1685 × 203** (hd'nin tam 2 katı) |

> İkisini de üret: oyun "hd" ve "uhd" atlaslarını birlikte kullanır. uhd = hd × 2.

## 3) Adım adım: logoyu değiştirme

```bash
# 1) Tüm kareleri şablon olarak çıkar
python3 plist-plaka.py --tumu /yol/GJ_LaunchSheet-hd.plist /yol/GJ_LaunchSheet-hd.png sablon-hd/
python3 plist-plaka.py --tumu /yol/GJ_LaunchSheet-uhd.plist /yol/GJ_LaunchSheet-uhd.png sablon-uhd/
```

2. `sablon-hd/GJ_logo_001.png` dosyasını **Photoshop/Figma/GIMP**'te aç, logonu aynı tuvale çiz
   (843×102). Şeffaf arka planı koru (PNG-24 + alfa).
3. Aynısını `sablon-uhd/GJ_logo_001.png` (1685×203) için yap — **hd'nin 2 katı çözünürlük**.
4. Şimdi spritesheet'i yeniden kur. İki yol:

   **Yol A — en kolay (plist düzenlemesi gerekmez):** Kendi logonu, orijinal karenin
   *kapladığı alanı değiştirmeden* yerleştir: yani `GJ_LaunchSheet-hd.png`'yi kopyala,
   sadece logo karesinin bulunduğu dikdörtgeni kendi logonla üzerine yaz (aynı boyut).
   Plist aynen kalır → hizalama bozulmaz. ✅ Önerilen.
   ```python
   # örnek: kare koordinatlarını plist'ten oku, üzerine yaz
   from PIL import Image
   sheet = Image.open("GJ_LaunchSheet-hd.png").convert("RGBA")
   logo  = Image.open("kendi-logom-843x102.png").convert("RGBA")
   sheet.paste(logo, (X, Y), logo)          # X,Y = plist'teki textureRect köşesi
   sheet.save("turkce-tema/GJ_LaunchSheet-hd.png")
   ```

   **Yol B — plist'i güncelle:** Kendi logonun boyutu farklıysa plist'teki
   `textureRect` / `spriteSourceSize` değerlerini yeni boyutlara göre düzenle.
   (Format 3 plist: `{{x,y},{w,h}}` biçiminde.)

5. Paketi test et: Texture Loader → paketi seç → **Apply** → oyunu yeniden başlat.

## 4) Ne değiştirilebilir — öneri listesi (etki/güvenlik dengesi)

| Öncelik | Öğe | Dosya | Not |
|---|---|---|---|
| ⭐⭐⭐ | Ana logo | `GJ_LaunchSheet-hd/uhd` | En görünür, en çok istek gören |
| ⭐⭐⭐ | Arka plan | `GJ_gradientBG-hd/uhd.png` | Türk bayrağı kırmızısı → beyaz gradyan; tek PNG, kolay |
| ⭐⭐ | Buton zemini | `GJ_button_01..06`, `GJ_square01..05` | Tüm menünün havasını değiştirir |
| ⭐⭐ | Yükleme ekranı | `LoadingLayer` görselleri | İlk izlenim |
| ⭐⭐ | Simge/ikonlar | `GJ_GameSheet03` içindeki `*Btn` / `*Icon` | 612 kare; seçerek değiştir |
| ⭐ | Zorluk yüzleri | `GJ_GameSheet04` | Şeytan/çılgın ikonları |
| ⭐ | Oyun içi | `GJ_GameSheet` (`GJ_groundSquare`, `GJ_square`, portal/trigger) | Dikkat: oynanabilirliği bozma |
| ❌ | Orijinal level/şarkı dosyaları | `Resources` | Dokunma |

> **İpucu:** Oyun içi (gameplay) doku değiştirmek en riskli alan. Önce **sadece menü**
> katmanında paket yayınla; beğenilirse "gameplay skin" ayrı paket olarak çıksın.

## 5) Türkiye'ye özgü paket fikirleri

1. **"Türk Bayrağı UI"** — kırmızı-beyaz gradyan arka plan + ay-yıldız motifli logo + kırmızı
   buton zemini. En çok indirme potansiyeli olan, en kolay iş.
2. **"Anadolu Teması"** — kilim/halı desenli butonlar, lacivert-turkuaz palet (ekran görüntüsünde
   çok iyi durur, "kültürel" algı yüksek).
3. **"Bayram Teması"** — 23 Nisan / 29 Ekim / Ramazan için mevsimsel sürüm. Topluluk
   etkinliklerinde paylaşılınca hızlı yayılır.
4. **"İstanbul"** — silüet arka planı (galata/köprü), menü müziği önerisi listesiyle birlikte.

## 6) Yasal not (önemli)

- Orijinal spritesheet'leri **dağıtma**. Paketinde yalnızca **senin ürettiğin** görseller olsun.
  (Orijinal atlası kopyalayıp üzerine çizip yayınlamak = telif ihlali.)
- Kendi spritesheet'ini plist ile birlikte üretirken görseller tamamen sana ait olmalı.
- RobTop logosu, GD logosu gibi tescilli markaları **kendi logonla değiştir**, taklit etme.
- Paketi ücretsiz yayınla; Geode/Texture Loader ekosisteminde ücretli paket yok.

## 7) Paket yapısı (örnek)

```
turkce-tema/
├── pack.json
├── pack.png
├── GJ_LaunchSheet-hd.png      + GJ_LaunchSheet-hd.plist     (logo)
├── GJ_LaunchSheet-uhd.png     + GJ_LaunchSheet-uhd.plist
├── GJ_gradientBG-hd.png                                     (arka plan)
├── GJ_gradientBG-uhd.png
├── GJ_button_01-hd.png ... (butonlar)
└── bigFont-hd.fnt + _0.png, goldFont-hd.fnt + _0.png        (font, ayrı paket de olabilir)
```

`pack.json`:
```json
{
	"textureldr": "1.5.0",
	"name": "Türkçe Tema",
	"id": "kullaniciadi.turkce-tema",
	"version": "1.0.0",
	"author": "KullanıcıAdı"
}
```

Zip'lerken **dosyalar kök dizinde** olmalı (klasörsüz).
