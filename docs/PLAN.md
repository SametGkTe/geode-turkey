# Geode'u Türkçeleştirme — Uygulanabilir Plan (v1)

**Tarih:** 8 Kasım 2026 · **Hedef:** Geode mod menüsünü Türkçe yapmak, disk/kota sınırını zorlamadan, üstüne Türkiye'ye özgü bir katkı koymak.

---

## 1) Kısa cevap (TL;DR)

> **Senin seçimin: Windows + Android, bulutta derleme, menü çevirisi + Geode'a kalıcı `tr` desteği PR'ı.**
>
> **En kolay yol: Geode loader'ı forklamak değil, sahnedeki yazıları çeviren küçük bir mod yazmak** ve onu **GitHub Actions'ta bulutta derlemek** (PC'de Geode SDK/derleyici kurmadan). Bu repoda o modun iskeleti + 250'den fazla hazır Türkçe çeviri + hata denetleyen araç hazır. Sana kalan: GitHub'a atıp Actions'ı çalıştırmak (~10 dakika) ve `.geode` dosyasını mods klasörüne bırakmak.

**Kapsam artık 3 katman + 2 görsel paket:**
1. **Geode arayüzü** çevirisi (254 metin) — runtime mod
2. **Oyunun kendi menüleri** (ayarlar, hesap, profil, seviye ekranları — 213 metin) — aynı mod, GlobalID güvenlik kilidiyle
3. **Geode'a kalıcı `tr` desteği** PR'ı (`tr.po` hazır)
4. **Türkçe font paketi** — `bigFont.fnt`'de eksik olan **tam 6 glif**: `ı İ ş Ş ğ Ğ`
5. **Logo + oyun içi görsel paketi** — Türk temalı Texture Loader paketi

Disk: toplam çalışma alanı **~300 KB**; derleme bulutta.

---

## 2) Gerçek durum tespiti (kaynağa bakarak doğruladım)

| Soru | Cevap |
|---|---|
| Geode arayüzü çevrilebilir mi? | **Şu an hayır.** `geode-sdk/geode` deposunda (main, v6.0.0-alpha.1) gettext/`.po`/`.json` dil dosyası **yok**; mod menüsü metinleri C++ koduna gömülü (`"Install"`, `"Restart Required"`, `<cy>...` etiketli paragraflar). |
| Yani resmî bir dil seçeneği var mı? | Geode loader UI'ında **yok**. (Geode'un sadece *Windows kurulum sihirbazında* dil dosyaları var — `TurkishExtra.nsh` dahil. O, oyun içi menüyü etkilemez.) |
| Geode mod indeksinde Türkçe çeviri modu var mı? | **Yok.** 985 modun tamamını taradım; "translation / localization / Turkish / çeviri" geçen tek şey `darkping.integrated_turklist` (Türk Demonlist entegrasyonu). Yani alan boş — ilk olma şansı yüksek. |
| Oyunun kendisi Türkçe mi? | GD 2.2081+ sürümlerinde dil listesinde Türkçe görünüyor. **Ama** Geode menüsü oyunun dil sisteminin dışında, kendi çizdiği yazıları kullanıyor. Yani "oyunu Türkçe yaptım, Geode da Türkçe oldu" olmuyor. |
| Loader'a mı dokunmak gerek? | Hayır. Loader'ı fork edip derlemek hem çok riskli (anti-cheat/ban muhabbeti, her GD güncellemesinde kırılır) hem de diskte GB'larca alan ister. **Yapma.** |

**Sonuç:** Doğru mimari = *runtime çevirici mod*. Oyun açılır, mod sahne ağacını gezip etiketleri çevirir. Geode güncellense de çalışır, dağıtımı tek `.geode` dosyasıdır.

---

## 3) Yaklaşımların karşılaştırması

| | **A) Runtime çevirici mod** (önerilen) | B) Loader fork + derleme | C) Upstream'e `tr` desteği PR'ı |
|---|---|---|---|
| Zorluk | Düşük (C++ ama ~200 satır) | Çok yüksek | Orta–yüksek |
| Disk ihtiyacı | **~5 MB** (metin + repo; derleme bulutta) | 15–25 GB (SDK, MSVC, cache) | ~2 GB |
| Kırılganlık | Düşük (etiket bulamazsa hiçbir şey yapmaz) | Her GD/Geode sürümünde kırılır | Orta |
| Kapsam | Geode menüsü + popuplar + açıklama metinleri | Her şey | Her şey, kalıcı |
| Yayınlanabilirlik | Geode indeksine mod olarak **evet** | Hayır (özel build) | Geode'un kendisi |
| Not | Mağaza açıklamaları sunucudan geldiği için İngilizce kalır | Önerilmez | Uzun vadeli doğru çözüm |

**Karar: A ile başla, C'yi paralel yürüt** (A sana hızlı sonuç verir; C topluluğa kalıcı katkı olur ve CV/reputation için değerlidir).

---

## 4) Bu pakette şu an hazır olanlar

```
geode-tr/
├── PLAN.md                 ← bu dosya
├── mod/                    ← GitHub repo köküne atılacak mod (Geode arayüzü + oyun menüleri)
│   ├── README.md · mod.json · CMakeLists.txt · about.md · changelog.md
│   ├── src/
│   │   ├── main.cpp                 iki katmanlı runtime çevirici
│   │   ├── translations.generated.hpp   Geode arayüzü (254)  — OTOMATİK
│   │   └── vanilla.generated.hpp        Oyun menüleri  (213)  — OTOMATİK
│   ├── ceviriler/
│   │   ├── ceviri-tablosu.tsv       Geode arayüzü çevirileri
│   │   ├── vanilya-tablosu.tsv      Oyunun kendi menüleri (ayarlar/hesap/profil...)
│   │   └── geode-kaynak-metinler.tsv  Geode'dan çıkarılmış ham metinler
│   ├── glossary.tsv · arac/ (üretici + denetleyici + po üretici)
│   ├── upstream/                    Geode'a tr desteği PR paketi (tr.po, rehber)
│   └── .github/workflows/           Windows + Android32/64 bulut derlemesi
└── tema-tr/                ← logo + oyun içi görsel + font paketi çalışma alanı
    ├── TEMA-REHBERI.md              logo/doku değişimi, Türk temalı paket fikirleri
    ├── FONT-NOTLARI.md              FontCreator ile 6 eksik glif (ı İ ş Ş ğ Ğ)
    ├── plist-plaka.py               spritesheet'ten tek kare çıkarma aracı
    └── sablon/                      orijinal logo şablonları (843×102 ve 1685×203)
```

**Bugünkü durum: 467 çeviri** (Geode 254 + oyun 213), 0 hata, 7 uyarı.

```bash
cd mod
python3 arac/ceviri-olustur.py            # iki sözlüğü üret + denetle
python3 arac/ceviri-olustur.py --kontrol  # sadece denetle
python3 arac/po-olustur.py                # upstream/tr.po üret
cd ../tema-tr
python3 plist-plaka.py --liste /yol/GJ_LaunchSheet-hd.plist   # kareleri listele
```

## 5) Senin yapman gerekenler (≈30 dakika, disk yükü yok)

### 5.1 Derleme — bulutta (önerilen, PC'de 0 MB ek yük)

1. GitHub hesabı aç, yeni **private** repo oluştur (ör. `geode-tr`).
2. `mod/` klasörünün **içeriğini** repo köküne at (Actions dosyası `.github/` altında olduğu için kök önemli):
   ```bash
   cd geode-tr/mod
   git init && git add . && git commit -m "ilk sürüm"
   git branch -M main
   git remote add origin https://github.com/<kullanıcı>/geode-tr.git
   git push -u origin main
   ```
3. Repo sayfası → **Actions** → "Build Geode Mod" → **Run workflow**. (Workflow Windows + Android32/64 için ayarlı; çeviri denetimi de çalışır.)
4. ~10–20 dakika sonra **Artifacts → Build Output** altında platforma uygun `.geode` dosyaları hazır (`...win.geode`, `...android32.geode`, `...android64.geode`).
5. Dosyayı GD'nin Geode klasöründeki `mods` dizinine bırak (Windows'ta genelde `%LOCALAPPDATA%\Geode\mods`), oyunu aç → Mod Menüsü Türkçe.

> Derleme bulutta olduğu için Geode SDK (birkaç GB) **senin diskine hiç inmez**. Tek şart: repo'da `mod.json` ve `CMakeLists.txt` doğru olsun.

### 5.2 Yerel derleme istersen (disk sınırı olan biri için püf nokta)

- Visual Studio **değil**, sadece **Geode CLI + clang** yeterli: `geode-sdk/cli` kullanarak `geode build` çalıştırabilirsin; MSVC'nin ~8 GB'lık kurulumuna gerek kalmaz.
- Build klasörünü iş bitince sil (`rm -rf build`), `.geode` çıktısını başka yere kopyala. Tipik mod build klasörü 300–800 MB.
- `geode.exe` / SDK indirmesini **tek seferlik** yapıp `%USERPROFILE%\.geode` dışına kurma; orada cache'lenir ve güncellemelerde yeniden indirmez.

### 5.3 Kişiselleştirme (zorunlu küçük işler)

- `mod/mod.json`: `id` (ör. `seninadin.geode-tr`), `name`, `developer` alanlarını doldur. `geode` alanını kullandığın Geode SDK sürümüne göre ayarla.
- Bir `logo.png` (512×512) ekle — indekse yüklerken isteniyor.

---

## 6) Görsel katman: logo, oyun içi ve oyun menüleri

### 6.1 Oyunun kendi menüleri (ayarlar, hesap, profil) — ÇÖZÜLDÜ
- GD'nin metinleri koda gömülü; en pratik yol **etiket metinlerini değiştirmek** (bu mod yapıyor).
- **Güvenlik kilidi:** vanilla çeviri yalnızca Geode'un **GlobalID'si açıkken** çalışır. Sebep:
  kullanıcı adları/seviye isimleri de etiket — GlobalID olmadan yanlış çeviri riski var.
  GlobalID kapatılınca mod otomatik olarak yazıları **İngilizceye geri alır**.
- Ayarlardan `vanilla-ceviri` kapatılarak tamamen devre dışı bırakılabilir.
- Kapsanan ekranlar: ana menü butonları, Seçenekler, Hesap/Giriş, Profil, İstatistikler,
  Seviye bilgisi, Editör seçenekleri, Duraklat menüsü, Mağaza/Görevler/Başarımlar temel terimleri.

### 6.2 Türkçe font — eksik glifler kanıtlandı
`bigFont-hd.fnt` içinde **188 karakter** var: ASCII + **Latin-1 tamamı**. Yani `ç ö ü Ç Ö Ü`
zaten mevcut. **Eksik olan sadece 6 glif: `ı (U+0131)`, `İ (U+0130)`, `ş (U+015F)`, `Ş (U+015E)`,
`ğ (U+011F)`, `Ğ (U+011E)`.** FontCreator iş akışı `tema-tr/FONT-NOTLARI.md` içinde.

### 6.3 Logo & oyun içi görseller
En sık yapılan hata: logoyu `GJ_logo_001.png` diye tek dosya koymak — **çalışmaz**, çünkü logo
`GJ_LaunchSheet-hd.plist` **spritesheet'i** içinde. Doğrusu `GJ_LaunchSheet-hd.png + .plist`
ikilisini paketlemek. Orijinal logo karesini plist'ten çıkardım, **tam ölçüler**:
**843×102 (hd)** ve **1685×203 (uhd)** — şablonlar `tema-tr/sablon/` içinde.
Detaylı adımlar + Türk temalı paket fikirleri: `tema-tr/TEMA-REHBERI.md`.

### 6.4 Türkiye'ye özgü katkı fikirleri
1. **⭐ Geode'a gerçek `tr` desteği PR'ı** — kalıcı, tüm kullanıcılar için; `tr.po` hazır.
2. **⭐ Türkçe font paketi** — 6 glif; sadece Geode'u değil Türkçe seviye isimlerini de düzeltir.
3. **⭐ Türk Bayrağı / Anadolu temalı UI paketi** — arka plan + logo + buton zemini.
4. **Türkçe doküman + terim standardı** (`glossary.tsv`).
5. **TR mod paketi** ve Türk yapımcı tanıtımı (`integrated_turklist` ile çapraz).

---

## 7) Çeviri yaparken dikkat (bunlar başına iş açabilir)

1. **Renk etiketleri bozulmaz:** `<cy>`, `<cr>`, `<cg>` ... `</c>` etiketleri korunmalı. Aracı her seferinde kontrol ediyor.
2. **Yer tutucular:** `{}`, `{0}`, `{:.100}` aynen kalmalı; sıra değişebilir ama sayı değişmez. (`{}` sayısı tutmayan 5 satırı bilerek `elle` olarak işaretledim — onlar çalışma anında `fmt` ile birleştiği için birebir eşleşmez.)
3. **Bitmap font taşması:** Türkçe İngilizceden ~%20–30 uzun. Buton metinlerinde kısa tut (`Install → Yükle`, `Uninstall → Kaldır`). Araç 2×+12 karakteri aşanları uyarı olarak listeliyor.
4. **`\n` sayısı:** çok satırlı popup metinlerinde satır sayısını koru, yoksa metin kutudan taşar.
5. **Türkçe `I/ı` tuzağı (Türkiye'ye özgü teknik risk):** `tolower`/`toupper` kullanan kod, `tr_TR` yerel ayarında `I → ı` yapar ve eşleştirmeler bozulur. Modda bilinçli olarak `tolower` **kullanmadım**; sen de kullanma, ASCII karşılaştırma yap. (Aynı hata yüzünden Windows'ta Türkçe yerel ayarda bazı derleme araçları da sapıtabilir — CI'da `LANG`/locale ayarını `en_US` bırak.)
6. **Terim tutarlılığı:** "Mod" kelimesini çevirme (topluluk "mod" diyor). `glossary.tsv` tek doğru kaynak olsun; her yeni metin önce oraya bakar.
7. **Mağaza açıklamaları çevrilmez:** onlar sunucudan gelir (İngilizce). Bunu README'de dürüstçe belirt, kullanıcı "eksik çeviri" diye şikâyet etmesin.

---

## 8) Sonraki adımlar (sırayla)

1. `mod/mod.json` alanlarını doldur, `logo.png` ekle.
2. GitHub'a at, Actions'ı çalıştır, `.geode`'u indir, oyunda dene.
3. Ekran görüntüsü al → hangi metinler hâlâ İngilizce? Onları `ceviri-tablosu.tsv`ye ekle, tekrar derle. (**Döngü bu: tablo → araç → build → test.**)
4. Kararlı çalışınca Geode indeksine yükle (`geode-sdk.org/mods`, "Submit a mod").
5. Paralel: font paketi (②) ve `tr` desteği PR'ı (①).

---

## 9) Yasal/etik notlar

- GD'nin orijinal dosyalarını (özellikle font atlaslarını) **paylaşma**; font paketinde kendi ürettiğin atlası dağıt.
- Modu ücretsiz yayınla; "ücretli içerik" işaretleme yok, Geode ödemeleri işlemiyor.
- Geode indeksi mod incelemesi yapar; `about.md` + `changelog.md` eklemen istenebilir.

---

## 10) Seçtiğin yol (bu pakete göre)

| Karar | Seçim | Sonuç |
|---|---|---|
| Platform | Windows + Android | Workflow Win64 + Android32/64'e daraltıldı (macOS/iOS yok → daha hızlı build) |
| Derleme | GitHub Actions (bulut) | PC'de 0 MB ek yük; SDK indirmesi yok |
| Kapsam | Menü çevirisi **+ Geode'a `tr` desteği PR'ı** | Mod hızlı sonuç; PR kalıcı çözüm. `upstream/` klasörü ve `tr.po` hazır |

### Önerilen sıra
1. **Bugün:** `mod/mod.json` alanlarını doldur → repo → Actions → `.geode` → oyunda test (mod ile Türkçe menü).
2. **Bu hafta:** eksik metinleri tabloya ekle, döngüyü oturt (tablo → araç → build → test).
3. **Paralel:** Geode Discord'unda/issue'da "localization support + Turkish" konuşmasını başlat
   (`upstream/PR-REHBERI.md` §1 ve §5'teki taslak mesajı kullan).
4. **PR #1:** yalnızca i18n API iskeleti (~300 satır `en.json` ile) — tek başına gözden geçirilebilir.
5. **PR #3:** `tr.json` (bizim 259 metin) → Türkçe kalıcı olur, mod "hızlı çözüm" olarak kalır.
6. İsteğe bağlı: Türkçe font paketi (ş/ğ/İ/ı) — ayrı mod olarak.

---

### Doğrulanmış kaynaklar
- `geode-sdk/geode` deposu (main branch, sürüm dosyası `6.0.0-alpha.1`): loader UI metinleri koda gömülü; `translations/`, `.po`, `i18n` izi yok.
- Yalnızca `installer/windows/Language Files/TurkishExtra.nsh` var (Windows kurulum sihirbazı dili).
- Geode mod indeksi API taraması (985 mod): Türkçe/çeviri modu bulunamadı.
- `geode-sdk/template-mods` + `build-geode-mod` action: bulutta derleme akışı (workflow bu repoda aynen kullanılıyor).
- `geode-sdk/bindings` (2.2081): `CCLabelBMFont::setString(char const*, bool)` ve `CCLabelTTF` erişilebilir → runtime çeviri teknik olarak mümkün.
