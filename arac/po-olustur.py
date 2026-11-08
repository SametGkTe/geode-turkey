#!/usr/bin/env python3
"""
po-olustur.py — Çeviri tablosundan gettext .po dosyası üretir.

Bu dosya iki işe yarar:
  1) Geode'a yapılacak "gerçek tr dil desteği" PR'ında kullanılacak `tr.po`
  2) Poedit/Weblate/Transifex gibi araçlarla çeviri düzenlemek isteyenler için
     standart format

Kullanım:
    python3 arac/po-olustur.py

Girdi : glossary.tsv + ceviriler/ceviri-tablosu.tsv
Çıktı : upstream/tr.po  (+ upstream/messages.pot şablonu)
"""

import csv, pathlib, datetime, re

KOK = pathlib.Path(__file__).resolve().parent.parent
GIRDI = [KOK / "glossary.tsv", KOK / "ceviriler" / "ceviri-tablosu.tsv"]
CIKTI_DIZIN = KOK / "upstream"

BASLIK = '''# Geode Türkçe yerelleştirme dosyası
# Bu dosya Geode'un loader UI metinlerini Türkçeye çevirir.
# Kaynak metinler: geode-sdk/geode @ main, loader/src/ui altındaki dizeler.
# Katkı: ceviriler/ceviri-tablosu.tsv dosyasını düzenleyip
#        python3 arac/po-olustur.py çalıştırın.
msgid ""
msgstr ""
"Project-Id-Version: Geode (Türkçe)\\n"
"Report-Msgid-Bugs-To: https://github.com/geode-sdk/geode/issues\\n"
"POT-Creation-Date: {tarih}\\n"
"PO-Revision-Date: {tarih}\\n"
"Last-Translator: {yazar}\\n"
"Language-Team: Türkçe\\n"
"Language: tr\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
"Plural-Forms: nplurals=2; plural=(n > 1);\\n"
'''

YAZAR = "Geode Türkçe Topluluğu <ornek@example.com>"


def oku(yol):
    kayitlar = []
    if not yol.exists():
        return kayitlar
    with open(yol, encoding="utf-8") as f:
        for satir in csv.DictReader(f, delimiter="\t"):
            en = (satir.get("EN") or satir.get("msgid") or "").strip()
            tr = (satir.get("TR") or satir.get("msgstr") or "").strip()
            if not en or not tr:
                continue
            kayitlar.append((en, tr, str(yol.name)))
    return kayitlar


def kacisla(s):
    """TSV'deki metin C++ kaynağından geldiği için '\\n' dizisi zaten kaçışlı.
    PO'da da aynı şekilde görünmesi gerekir; sadece '"' kaçışlanır."""
    return s.replace('"', '\\"')


def satir_yaz(anahtar, deger):
    """.po formatı: uzun metinler satır satır bölünür."""
    return f'{anahtar} "{kacisla(deger)}"\n'


def uret(kayitlar, tarih):
    parcalar = [BASLIK.format(tarih=tarih, yazar=YAZAR), "\n"]
    gorulen = set()
    for en, tr, _ in sorted(kayitlar):
        if en in gorulen:
            continue
        gorulen.add(en)

        # PO yorumu: kaynak metin çok satırlıysa editörde görünsün
        parcalar.append("#. Kaynak tabloda: ceviriler/ceviri-tablosu.tsv\n")
        parcalar.append(satir_yaz("msgid", en))
        parcalar.append(satir_yaz("msgstr", tr))
        parcalar.append("\n")
    return "".join(parcalar)


def uret_pot(kayitlar, tarih):
    parcalar = [BASLIK.format(tarih=tarih, yazar=YAZAR).replace(
        '"Language: tr\\n"', '"Language: \\n"').replace(
        '"Plural-Forms: nplurals=2; plural=(n > 1);\\n"', '')]
    parcalar.append("\n")
    for en, _tr, _ in sorted(kayitlar):
        parcalar.append(satir_yaz("msgid", en))
        parcalar.append('msgstr ""\n\n')
    return "".join(parcalar)


def main():
    kayitlar = []
    for yol in GIRDI:
        kayitlar += oku(yol)

    # tekrarları temizle
    tekil = {}
    for en, tr, d in kayitlar:
        tekil.setdefault(en, (en, tr, d))
    kayitlar = list(tekil.values())

    tarih = datetime.datetime.now().strftime("%Y-%m-%d %H:%M%z") or "2026-11-08 00:00+0000"
    CIKTI_DIZIN.mkdir(parents=True, exist_ok=True)
    (CIKTI_DIZIN / "tr.po").write_text(uret(kayitlar, tarih), encoding="utf-8")
    (CIKTI_DIZIN / "messages.pot").write_text(uret_pot(kayitlar, tarih), encoding="utf-8")
    print(f"{len(kayitlar)} çeviri yazıldı → upstream/tr.po, upstream/messages.pot")


if __name__ == "__main__":
    main()
