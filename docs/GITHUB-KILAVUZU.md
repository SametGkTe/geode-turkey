# Yön haritası: GitHub → Actions → oyun, ve içerikleri kendin değiştirme

Bu dosya **"ben ne yapacağım, nerede neyi değiştireceğim?"** sorusunun tam cevabı.
Kod bilmen gerekmiyor; sadece 2 dosya türünü düzenleyeceksin: **`.tsv` tabloları** (çeviri)
ve **`.json`** (mod bilgileri).

---

## 0) Büyük resim — 4 adım, toplam ~40 dakika (bir kere)

```
[1] Paketi repo'ya çevir         →  bash repoya-hazirla.sh
[2] GitHub'a yükle (push)        →  git remote add + git push
[3] GitHub Actions çalıştır      →  sekmeden "Run workflow"
[4] .geode dosyasını oyuna kur   →  mods klasörüne kopyala
```

Bundan sonraki döngü **çok kısa**: *tabloda çeviri düzelt → commit → Actions kendi derler → yeni `.geode` indir.*
Ortalama 10–15 dakika (derleme süresi), senin emeğin ~1 dakika.

> **Disk:** Bu akışta PC'ne Geode SDK, Visual Studio, Python **kurman gerekmiyor**.
> Derleme GitHub'ın sunucusunda olur. Tek indirdiğin şey birkaç MB'lık `.geode` dosyası.

---

## 1) Paketi repo haline getir

Bu klasörün içindeyken:

```bash
cd geode-tr
bash repoya-hazirla.sh
```

Bu komut:
- `geode-tr-repo/` adında yeni bir klasör oluşturur,
- mod dosyalarını **repo köküne** koyar (Actions'ın çalışması için şart),
- `docs/` altına planı ve tema rehberlerini koyar,
- `.gitignore` yazar,
- çeviri sözlüklerini üretir,
- `git init` + ilk commit'i atar.

**Windows kullanıyorsan:** Git Bash (Git for Windows ile gelir) içinde aynı komutu çalıştır.
PowerShell'de `bash` yoksa: `git-bash` aç, `cd` ile klasöre gel.

---

## 2) GitHub'a yükle

### a) GitHub'da boş repo aç
1. github.com → sağ üst **+** → **New repository**
2. İsim: `geode-tr` · **Private** seçebilirsin (Actions ücretsiz kotadan çalışır)
3. **README / .gitignore / license EKLEME** (boş kalsın) → **Create repository**

### b) Push et (komut satırı)

```bash
cd geode-tr-repo
git remote add origin https://github.com/KULLANICI/geode-tr.git
git push -u origin main
```

Şifre yerine **Personal Access Token** ister (GitHub 2021'den beri): Settings → Developer settings
→ Personal access tokens → Tokens (classic) → Generate new token → `repo` yetkisi → kopyala, şifre alanına yapıştır.

### c) Komut satırı istemiyorsan: web'den yükle
1. Boş repo sayfasında **uploading an existing file**
2. `geode-tr-repo` klasörünün **içindekileri** sürükle-bırak (klasörün kendisini değil, içeriğini)
3. ⚠️ Gizli klasör `.github/` web yüklemede **kaybolabilir**. Yükleme sonrası
   **Add file → Create new file** → adı: `.github/workflows/multi-platform.yml`
   → içeriğini `mod/.github/workflows/multi-platform.yml`'den kopyala-yapıştır.
   (Bu dosya olmadan Actions hiç çalışmaz.)

---

## 3) Actions ile derleme

1. Repo → üstte **Actions** sekmesi
2. Sol listede **Build Geode Mod** → sağda **Run workflow** → **Run workflow**
3. ~10–20 dakika bekle. Yeşil tik = başarılı, kırmızı çarpı = hata (bölüm 6)
4. Repo ana sayfası → Actions → tamamlanan çalıştırma → sayfanın altındaki **Artifacts**
   → **Build Output** indir (zip)
5. Zip'ten çıkan `.geode` dosyaları:
   - `...win.geode` → Windows
   - `...android32.geode` / `...android64.geode` → Android

### Oyuna kurma
| Platform | Klasör |
|---|---|
| Windows | `%LOCALAPPDATA%\Geode\mods` (adres çubuğuna bu yolu yapıştır) |
| Android | `Android/data/com.robtopx.geometryJump/files/geode/mods` (Geode sürümüne göre değişebilir; Geode ayarlarında "Open mods folder" da var) |

Dosyayı at → oyunu aç → Geode menüsü Türkçe. İlk açılışta Türkçe font uyarısı çıkarsa normaldir (bölüm 5.2).

---

## 4) İÇERİKLERİ KENDİN DEĞİŞTİRME — asıl bölüm

### 4.1 Hangi dosya neyi değiştirir? (tek bakışta)

| Ne değiştirmek istiyorum? | Düzenlenecek dosya |
|---|---|
| Geode menüsündeki bir çeviri | `ceviriler/ceviri-tablosu.tsv` |
| Oyun menülerindeki (ayarlar/hesap/profil) çeviri | `ceviriler/vanilya-tablosu.tsv` |
| Bir terimin her yerde aynı olması (ör. "mod") | `glossary.tsv` |
| Modun adı, yazarı, sürümü, ayarları | `mod.json` |
| Mağaza sayfası metni | `about.md` |
| Sürüm notları | `changelog.md` |
| Çeviri kodunu/mantığını | `src/main.cpp` (dikkat: derleme gerekir) |
| Logo, font, tema (ayrı paket) | `docs/tema-tr/` rehberleri |

### 4.2 Tablo formatı (`.tsv` = Excel gibi, sekmeyle ayrılmış)

```
EN	TR	durum	not
Install	Yükle	hazir	
Restart Required	Yeniden Başlatma Gerekli	hazir	
```

| Sütun | Anlamı |
|---|---|
| **EN** | Oyundaki/Geode'daki **birebir** İngilizce metin. Harfi harfine aynı olmalı (büyük/küçük harf dahil). |
| **TR** | Türkçesi. Boş bırakırsan o metin çevrilmez. |
| **durum** | `hazir` → kullanılır · `elle` → **atlanır** (kod içinde birleştirilen metinler için) |
| **not** | Kendine not; program yok sayar. |

**Kurallar (denetleyici bunları kontrol ediyor):**
- `{}`, `{0}`, `{:.100}` gibi **yer tutucular aynen kalmalı**.
- `<cr>`, `<cg>`, `<cy>`, `<cl>`, `<cp>`, `<co>`, `<cb>`, `<cc>`, `<cj>`, `<ca>` renk etiketleri ve
  kapanışı `</c>` **korunmalı**. (`<cd>` diye yazma — `</cd>` yoktur, hepsi `</c>` ile kapanır.)
- `\n` (satır sonu) sayısı korunmalı.
- Buton metinleri kısa olmalı; 2×+12 karakteri geçen çeviriler uyarı alır.

### 4.3 Üç tipik iş — adım adım

#### (A) Mevcut bir çeviriyi düzeltmek — **en sık yapacağın şey**
Telefondan bile yapılabilir:
1. GitHub'da repoya gir → `ceviriler/ceviri-tablosu.tsv` dosyasına tıkla
2. Sağ üstte **kalem (Edit)** ikonu
3. `Install	Yükle` satırındaki Türkçe kısmı değiştir (ör. `Yükle` → `Yükle` yerine `Kur`)
4. Altta **Commit changes** → *Commit directly to the main branch* → **Commit**
5. Actions otomatik başlar; bitince yeni `.geode`'u indir.

> Satırlar arasında **boş satır bırakma**, **sekme** kullan (boşluk değil). Excel'de açıp
> kaydedersen sekmeleri korumaya dikkat et; en güvenlisi GitHub'ın kendi editörü.

#### (B) Yeni bir çeviri eklemek
1. Tabloya en alta satır ekle: `Settings	Ayarlar	hazir	`
2. EN sütununa İngilizceyi **birebir** yaz. Nereden bulacaksın?
   - `ceviriler/geode-kaynak-metinler.tsv` → Geode'un tüm ham metinleri + hangi dosyada olduğu
   - `ceviriler/vanilya-tablosu.tsv` dışında oyundan yeni metin görmek istersen:
     **GlobalID açıkken** o ekranı aç, İngilizce metni aklında tut, tabloya ekle
3. Commit → Actions.

#### (C) Oyun içinde hâlâ İngilizce kalan bir metin gördüm
1. O metni **birebir** not al (ör. `Delete all downloaded custom songs?`)
2. `vanilya-tablosu.tsv` içinde ara (GitHub'da `Ctrl+F` / dosya arama)
   - **Varsa:** TR sütunu boş veya `elle` işaretli → düzelt/`hazir` yap
   - **Yoksa:** yeni satır ekle
3. Commit → derle → tekrar bak.

### 4.4 Sözlükler (`generated.hpp`) — **elle dokunma**
`src/translations.generated.hpp` ve `src/vanilla.generated.hpp` otomatik üretilir.
Actions her çalıştığında tabloları tekrar okur, yani **tabloyu düzenlemen yeterli**.

Kendi bilgisayarında önizleme/denetim yapmak istersen (opsiyonel, Python varsa):

```bash
python3 arac/ceviri-olustur.py            # üret + denetle, hataları göster
python3 arac/ceviri-olustur.py --kontrol  # sadece denetle
```

### 4.5 Mod kimliği: `mod.json`
İlk iş **şunları değiştir**:
```json
"id": "kullaniciadi.geode-tr",     → "seninadin.geode-tr"
"name": "Geode Türkçe",            → istediğin isim
"developer": "KullanıcıAdı",       → senin adın
"version": "v0.2.0"                → her yayında artır
```
`id` **sonradan değiştirilirse** kullanıcıların kayıtlı ayarları sıfırlanır — bir kez belirle, sabit tut.

### 4.6 Logo / font / tema — ayrı bir paket
Bunlar `.geode` modu değil, **Texture Loader paketi** (zip). Akış farklı:
1. `docs/tema-tr/TEMA-REHBERI.md` (logo/görseller) ve `FONT-NOTLARI.md` (6 glif) rehberlerini izle
2. Görselleri üret, `pack.json` yaz, zip'le
3. Zip'i Texture Loader'ın `packs/` klasörüne at **veya** ayrı bir repoda yayınla

Aynı repoya koyacaksan: `tema/` klasörü açıp paket dosyalarını oraya koy (modun derlemesini etkilemez).

---

## 5) Sık yapılan işler — kısa tarifler

### 5.1 Yeni sürüm yayınlamak
1. `mod.json` → `version` artır (`v0.2.0` → `v0.3.0`)
2. `changelog.md` başına yeni sürüm bölümü ekle
3. Commit → Actions → yeni `.geode`

### 5.2 Türkçe harfler kutu görünüyor
Font eksik: `bigFont.fnt`'de `ı İ ş Ş ğ Ğ` yok (kanıtlandı: 188 karakter, ASCII+Latin-1).
`docs/tema-tr/FONT-NOTLARI.md` → FontCreator ile 6 glif → Texture Loader paketi.
Geçici çözüm: o metinlerde `ı→i`, `ş→s`, `ğ→g`, `İ→I` yaz (anlaşılır ama yanlış yazım).

### 5.3 Bir çeviri "fazla uzun, butona sığmıyor"
Tabloda kısalt. Mod zaten otomatik ölçek küçültüyor ama çok uzun metinlerde
küçük yazı okunmaz olur.

### 5.4 Ayar eklemek/çıkarmak
`mod.json` → `settings` bölümü. `src/main.cpp` içinde
`Mod::get()->getSettingValue<bool>("ayar-adi")` ile oku.

---

## 6) Bir şey ters gittiğinde

| Belirti | Sebep / çözüm |
|---|---|
| Actions hiç görünmüyor | `.github/workflows/multi-platform.yml` repoda yok (web yüklemede kayboldu). Elle oluştur. |
| Actions kırmızı, log'da `python3: command not found` | Workflow'da Python adımı var; repo kökünde `arac/` klasörünün olduğundan emin ol. |
| Log'da C++ hatası (`error:`) | `src/main.cpp` Geode sürümüyle uyuşmuyor olabilir. Hata satırını bana yapıştır — SDK sürümüne göre düzeltirim. |
| `mod.json` hatası | JSON'da virgül/parantez hatası. `python3 -m json.tool mod.json` ile doğrula. |
| Derleme başarılı ama `Artifacts` boş | "package" job'ına bak; genelde `combine` adımı hata verir. |
| Oyun açılmıyor | `.geode`'u kaldır, oyun açılıyorsa mod kaynaklı. Log: `%LOCALAPPDATA%\Geode\logs`. |
| Menü Türkçe ama bazı yerler İngilizce | O metin tabloda yok veya `elle` işaretli. Tabloya ekle (4.3-C). |
| Kullanıcı adları bozuldu | GlobalID kapalıyken vanilla çeviri denenmiş olabilir; mod GlobalID kontrolü yapıyor, ayarlardan `Oyun menülerini de çevir`'i kapat ve bildir. |

---

## 7) Günlük döngü (alıştıktan sonra 1 dakika)

```
Tabloda 1 satır düzelt  →  Commit  →  Actions (10-15 dk)  →  yeni .geode  →  oyunda test
```

İpucu: Tabloda **10-20 satırı birden** düzeltip tek commit at — her commit bir derleme demek.

---

## 8) Kod yazmadan ilerlemek istersen

| İhtiyaç | Yol |
|---|---|
| Çeviri düzelt/ekle | GitHub web editörü (telefon dahil) |
| Mod adı/sürüm | GitHub web editörü |
| Derleme | Actions (tek tık) |
| Logo/font | Kendi bilgisayarında görsel araçlar + zip |
| Yeni bir "hook" (kod) | Gerekmiyor; mevcut `main.cpp` ihtiyacı karşılıyor |

Yani **kod tarafına hiç dokunmadan** modu tamamen yönetebilirsin. Kodu sadece
"şu ekranda şu özel şey olsun" gibi yeni bir davranış istediğinde değiştiririz — onu da birlikte yaparız.

---

## 9) Kısa kontrol listesi (ilk yayın)

- [ ] `mod.json` → `id`, `name`, `developer` dolduruldu
- [ ] `logo.png` (512×512) eklendi (mağazaya yüklerken gerekir)
- [ ] Repo GitHub'da, `.github/workflows/` görünüyor
- [ ] Actions yeşil, `Build Output` indirildi
- [ ] `.win.geode` oyuna kuruldu, menü Türkçe
- [ ] Font uyarısı çıktıysa not alındı (font paketi sırada)
- [ ] Test edilenler: Geode menüsü · Seçenekler · Hesap · Profil · Duraklat
- [ ] Eksik metinler tabloya eklendi, ikinci derleme yapıldı
