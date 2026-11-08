> Bu repo, geode-tr paketinden uretildi.
> Plan ve gorsel/font rehberleri: docs/PLAN.md , docs/tema-tr/

# Geode TÃ¼rkÃ§e

Geode mod menÃ¼sÃ¼nÃ¼ **ve** oyunun kendi menÃ¼lerini TÃ¼rkÃ§eye Ã§eviren mod.
**467 Ã§eviri** hazÄ±r (Geode 254 + oyun 213), eksikler iÃ§in tablolar aÃ§Ä±k.

> âš ï¸ Durum: **v0.2** â€” kod derlenmeye hazÄ±r bir iskelettir; ilk gerÃ§ek SDK derlemesinde
> kÃ¼Ã§Ã¼k dÃ¼zeltmeler gerekebilir. Derleme bulutta (GitHub Actions) yapÄ±lÄ±r, diskinde ek yÃ¼k olmaz.

---

## Ne yapar / ne yapmaz

| Yapar | Yapmaz |
|---|---|
| **Geode mod menÃ¼sÃ¼** (254 metin): buton, popup, ayar, uyarÄ± | MaÄŸazadan gelen mod **aÃ§Ä±klamalarÄ±nÄ±** Ã§evirmez (sunucu Ä°ngilizce gÃ¶nderir) |
| **Oyunun kendi menÃ¼leri** (213 metin): SeÃ§enekler, Hesap, Profil, Ä°statistikler, seviye bilgisi, editÃ¶r | KullanÄ±cÄ± adlarÄ±nÄ± / seviye isimlerini Ã§evirmez (GlobalID kilidi) |
| TÃ¼rkÃ§e karakterler iÃ§in **font uyarÄ±sÄ±** gÃ¶sterir | Orijinal oyun dosyalarÄ±nÄ± deÄŸiÅŸtirmez |
| Ã‡eviri yoksa hiÃ§bir ÅŸeye dokunmaz (gÃ¼venli) | Oyunun `Resources` klasÃ¶rÃ¼ne yazmaz |

### Oyun menÃ¼leri nasÄ±l gÃ¼venli Ã§alÄ±ÅŸÄ±yor?
Vanilla Ã§eviri yalnÄ±zca Geode **GlobalID** modu aÃ§Ä±kken uygulanÄ±r (kullanÄ±cÄ± adlarÄ±, seviye
isimleri, yorumlar etiket olduÄŸu iÃ§in yanlÄ±ÅŸ Ã§eviri riski var). GlobalID kapatÄ±ldÄ±ÄŸÄ±nda mod
yazÄ±larÄ± otomatik olarak Ä°ngilizceye geri alÄ±r. Ayarlardan `Oyun menÃ¼lerini de Ã§evir`
kapatÄ±larak tamamen devre dÄ±ÅŸÄ± bÄ±rakÄ±labilir.

## HÄ±zlÄ± baÅŸlangÄ±Ã§ (Windows + Android, bulutta derleme)

```bash
# 1) Bu klasÃ¶rÃ¼n iÃ§eriÄŸini yeni bir GitHub reposuna at
cd mod
git init && git add . && git commit -m "Geode TÃ¼rkÃ§e v0.1"
git branch -M main
git remote add origin https://github.com/<kullanÄ±cÄ±>/geode-tr.git
git push -u origin main

# 2) GitHub â†’ Actions â†’ "Build Geode Mod" â†’ Run workflow
# 3) Artifacts â†’ Build Output â†’ .win.geode / .android64.geode indir
# 4) DosyayÄ± Geode mods klasÃ¶rÃ¼ne bÄ±rak, oyunu aÃ§
```

Windows'ta mods klasÃ¶rÃ¼ genelde: `%LOCALAPPDATA%\Geode\mods`
Android'de: `Android/data/com.robtopx.geometryjump/files/geode/mods` (Geode kurulumuna gÃ¶re deÄŸiÅŸebilir).

## Ã‡eviri dÃ¼zenleme (asÄ±l iÅŸ akÄ±ÅŸÄ±)

1. `ceviriler/ceviri-tablosu.tsv` dosyasÄ±nÄ± aÃ§ (Excel/Sheets/LibreOffice ile de olur).
2. SatÄ±r ekle/dÃ¼zelt: `EN <TAB> TR <TAB> durum <TAB> not`
   - `durum` alanÄ± `hazir` ise kullanÄ±lÄ±r; `elle` ise atlanÄ±r.
3. SÃ¶zlÃ¼ÄŸÃ¼ ve dosyayÄ± yeniden Ã¼ret:
   ```bash
   python3 arac/ceviri-olustur.py     # src/translations.generated.hpp Ã¼retir + denetler
   python3 arac/po-olustur.py         # upstream/tr.po Ã¼retir (Geode'a PR iÃ§in)
   ```
4. Commit + push â†’ Actions yeni `.geode` Ã¼retir.

### TÃ¼rkÃ§e karakterler gÃ¶rÃ¼nmÃ¼yorsa
Oyunun `bigFont.fnt` dosyasÄ±nda `Ä± Ä° ÅŸ Åž ÄŸ Äž` glifleri **yok** (188 karakter var: ASCII + Latin-1).
Mod aÃ§Ä±lÄ±ÅŸta bunu kontrol eder ve uyarÄ± gÃ¶sterir. Ã‡Ã¶zÃ¼m: **TÃ¼rkÃ§e Font Paketi** (Texture Loader).
Font Ã¼retimi: `../tema-tr/FONT-NOTLARI.md`.

### Denetleyici neleri yakalar?

- `{}` / `{0}` / `{:.100}` yer tutucularÄ±nÄ±n kaybolmasÄ± â†’ **hata**
- `<cr>...</c>` renk etiketlerinin bozulmasÄ± â†’ **hata**
- SatÄ±r sayÄ±sÄ± (`\n`) uyuÅŸmazlÄ±ÄŸÄ± â†’ uyarÄ±
- Butona sÄ±ÄŸmayacak kadar uzun Ã§eviri â†’ uyarÄ±

Hatalar dÃ¼zeltilmeden CI'da uyarÄ± Ã¼retilir; yerel Ã§alÄ±ÅŸtÄ±rmada Ã§Ä±kÄ±ÅŸ kodu `1` olur.

## Terimler

TutarlÄ±lÄ±k iÃ§in `glossary.tsv` tek doÄŸru kaynak. Ã–zet: **mod** (eklenti deÄŸil),
**Mod MenÃ¼sÃ¼**, **TuÅŸ AtamasÄ±**, **YÃ¼kle / KaldÄ±r / GÃ¼ncelle**, **Ã–ne Ã‡Ä±kan**.

## YapÄ±

```
mod/
â”œâ”€â”€ mod.json                 Geode manifesti (id / yazar / sÃ¼rÃ¼m burada)
â”œâ”€â”€ CMakeLists.txt
â”œâ”€â”€ src/
â”‚   â”œâ”€â”€ main.cpp             iki katmanlÄ± runtime Ã§evirici + font kontrolÃ¼
â”‚   â”œâ”€â”€ translations.generated.hpp   Geode sÃ¶zlÃ¼ÄŸÃ¼ â€” OTOMATÄ°K
â”‚   â””â”€â”€ vanilla.generated.hpp        Vanilla sÃ¶zlÃ¼ÄŸÃ¼ â€” OTOMATÄ°K
â”œâ”€â”€ ceviriler/
â”‚   â”œâ”€â”€ ceviri-tablosu.tsv   Geode arayÃ¼zÃ¼ Ã§evirileri (254)
â”‚   â”œâ”€â”€ vanilya-tablosu.tsv  Oyunun kendi menÃ¼leri (213)
â”‚   â””â”€â”€ geode-kaynak-metinler.tsv  Geode'dan Ã§Ä±karÄ±lmÄ±ÅŸ ham metin listesi
â”œâ”€â”€ arac/
â”‚   â”œâ”€â”€ ceviri-olustur.py    TSV â†’ C++ sÃ¶zlÃ¼k + denetleyici
â”‚   â””â”€â”€ po-olustur.py        TSV â†’ gettext (.po/.pot)
â”œâ”€â”€ upstream/                Geode'a PR iÃ§in: tr.po, messages.pot, PR rehberi
â””â”€â”€ .github/workflows/       Windows + Android32/64 derleme
```

## KatkÄ±

1. Ã‡eviri ekle â†’ tablo + `python3 arac/ceviri-olustur.py`
2. Oyun iÃ§i testte Ä°ngilizce kalan metni `ceviriler/geode-kaynak-metinler.tsv`
   iÃ§inde bul (kaynak dosya satÄ±rÄ± yazÄ±yor), tabloya ekle.
3. PR aÃ§. KÃ¼Ã§Ã¼k, tek konulu PR'lar tercih edilir.

## Lisans / notlar

- Orijinal oyun dosyalarÄ± (font atlaslarÄ± vb.) paylaÅŸÄ±lmaz.
- Bu mod Ã¼cretsizdir; Geode Ã¶deme iÅŸlemez.
- GD gÃ¼ncellemelerinden sonra Geode'un kendisi gÃ¼ncellenmeyi bekleyebilir â€” mod
  etiket bulamazsa hiÃ§bir ÅŸey yapmaz, oyunu bozmaz.

