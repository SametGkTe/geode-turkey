# Türkçe Font Paketi — FontCreator notları

Hedef: GD'nin `bigFont.fnt` ve `goldFont.fnt` bitmap fontlarına **6 eksik glifi** eklemek.
(Texture Loader paketi olarak yayınlanır; oyun dosyalarına dokunulmaz.)

---

## 1) Kanıt: tam olarak ne eksik?

GD 2.2.081'in `bigFont-hd.fnt` dosyasını ayrıştırdım: **188 karakter** var, ASCII + Latin-1
tam olarak mevcut. Yani **ç, ö, ü, Ç, Ö, Ü zaten var** — eklemeye gerek yok.

**Eksik olan 6 glif:**

| Harf | Unicode | Açıklama |
|---|---|---|
| ı | U+0131 | noktasız küçük i |
| İ | U+0130 | noktalı büyük I |
| ş | U+015F | s-cedilla |
| Ş | U+015E | S-cedilla |
| ğ | U+011F | g-breve |
| Ğ | U+011E | G-breve |

> ⚠️ Türkçede **i → İ** ve **I → ı** eşleşmesi kritik: "İptal", "İndir", "Işık".
> Font paketi olmadan bu harfler **kutu** olarak çıkar.

## 2) Çalışma akışı (FontCreator)

### a) Taban fontu bul
GD'nin bigFont'u **"Pusab"** fontudur (RobTop'un kullandığı ücretli font, GD dosyalarında
gömülü gelir). İki yol var:

- **Yol A (önerilen, temiz):** Kendi `.fnt`'ini sıfırdan üret. Latin Extended-A içeren
  benzer bir font kullan (ör. *Nunito Black*, *Baloo*, *Fredoka*) → 6 glif sorunsuz gelir,
  telif riski yok. Görsel olarak GD'ye %100 benzemez ama okunur ve yasaldır.
- **Yol B (birebir görünüm):** GD'nin kendi `bigFont-*.fnt` + `_0.png` atlasını al,
  FontCreator'da **Composite/Glyph** olarak 6 glifi ekle, atlası yeniden üret.
  ⚠️ Orijinal atlası **dağıtamazsın** (telif). Sadece *fark* olan bir yama yayınlamak da
  tartışmalı — bu yüzden Yol A daha güvenli.

### b) FontCreator'da ayarlar

1. **Yeni proje** → Units per em: **1000** (bitmap font için fark etmez, ihracı biz yapıyoruz).
2. **Glyph ekle:** `ı`, `İ`, `ş`, `Ş`, `ğ`, `Ğ` — *Insert → Glyphs* → Unicode kodlarıyla ekle.
   - `İ` için: mevcut `I` gövdesini kopyala + üstüne nokta (mevcut `i`'nin noktasından).
   - `ı` için: mevcut `i` gövdesini kopyala, noktayı sil.
   - `ş` için: `s` gövdesi + `ç`'nin çengeli (cedilla).
   - `ğ` için: `g` gövdesi + kısa breve (˘) — `g`'nin alt kuyruğu `y` gibi olabilir, dikkat.
3. **Metrikler:** `ş`, `ğ`, `ı` için `advance width` değerlerini kardeş harflerle aynı yap
   (`s` ile `ş` aynı genişlik → hizalama bozulmaz).
4. **Y-bearings:** Türkçe harflerin alt/üst taşmaları `lineHeight`'ı aşmasın; aşarsa
   GD'de satırlar üst üste biner.

### c) Bitmap font (.fnt) üretimi — KRİTİK

FontCreator `.fnt` **yazmaz**. İki seçenek:

- **Seçenek 1 — BMFont (AngelCode):** TTF/OTF'yi içe aktar, `bigFont` ile **aynı**
  boyut/padding ayarlarıyla atlas üret. Çıktı: `bigFont.fnt` + `bigFont_0.png`.
- **Seçenek 2 — mevcut .fnt'yi düzenle (Yol B):**
  1. `bigFont-hd.fnt`'yi metin editöründe aç.
  2. `chars count=188` → **194** yap.
  3. `char id=...` satırları ekle (alpha kanalından alınan x/y/w/h/offset).
  4. `_0.png` atlasına yeni glifleri yerleştir (sağ/sol boşluk kalmayacak şekilde).
  5. `common lineHeight`, `base` değerlerini değiştirme.

> Dosya adları oyunla **birebir** eşleşmeli: `bigFont-hd.fnt` + `bigFont-hd_0.png`,
> `bigFont-uhd.fnt` + `bigFont-uhd_0.png`, aynı şekilde `goldFont-hd/-uhd`.
> (uhd dosyaları `_0` ekli olmayabilir — kendi paketinde **olduğu gibi** kopyala.)

### d) Test (mutlaka)

1. Paketi Texture Loader'a at, oyunu aç.
2. Geode menüsünü Türkçe yap → şu metinleri kontrol et:
   - "İptal", "İndir", "Yükle", "Güncelle", "Şarkılar", "Değişiklik Günlüğü", "Işık"
3. Harflerin **kutu** değil, gerçek glif olarak göründüğünü doğrula.
4. Satır yüksekliği taşması var mı bak (ğ/ş alt taşması).

## 3) Kapsam: hangi dosyalar?

| Dosya | Neden |
|---|---|
| `bigFont-hd/-uhd` | Menü yazılarının %90'ı |
| `goldFont-hd/-uhd` | Altın renkli başlıklar / bazı ödül ekranları |
| `chatFont-hd` (varsa) | Sohbet — Türkçe yorumlar için bonus |

## 4) Paket yapısı (Texture Loader)

```
turkce-font/
├── pack.json
├── pack.png                (512x512, opsiyonel ama önerilir)
├── bigFont-hd.fnt
├── bigFont-hd_0.png
├── bigFont-uhd.fnt
├── bigFont-uhd_0.png
├── goldFont-hd.fnt
├── goldFont-hd_0.png
├── goldFont-uhd.fnt
└── goldFont-uhd_0.png
```

`pack.json`:
```json
{
	"textureldr": "1.5.0",
	"name": "Türkçe Font Paketi",
	"id": "kullaniciadi.turkce-font",
	"version": "1.0.0",
	"author": "KullanıcıAdı"
}
```

Zip'lerken dosyalar **kök dizinde** olmalı (klasör içinde değil), yoksa Texture Loader bulamaz.

## 5) Bu paketteki yardımcı araç

`plist-plaka.py` — GD spritesheet'lerinden tek kare çıkarır (logo vb. için, fontla ilgisi yok
ama aynı iş akışında işine yarar):

```bash
python3 plist-plaka.py --liste GJ_LaunchSheet-hd.plist        # kareleri listele
python3 plist-plaka.py GJ_LaunchSheet-hd.plist GJ_LaunchSheet-hd.png \
        "GJ_logo_001.png" sablon/GJ_LaunchSheet-hd.png        # şablon çıkar
```

`bigFont-*.fnt` içinde hangi karakterlerin olduğunu görmek için aynı mantıkla:
`grep "^char id=" bigFont-hd.fnt` → `id` değerleri Unicode kodlarıdır (351 = ş).
