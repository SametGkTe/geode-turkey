#!/usr/bin/env python3
"""
ceviri-olustur.py — Geode Türkçe çeviri tablolarından C++ sözlüğü üretir.

Kullanım:
    python3 arac/ceviri-olustur.py            # üret + denetle
    python3 arac/ceviri-olustur.py --kontrol  # sadece denetle (dosya yazmaz)

Girdi : glossary.tsv + ceviriler/ceviri-tablosu.tsv
Çıktı : mod/src/translations.generated.hpp
"""

import sys, re, csv, pathlib

# Windows konsolu (cp1252) Türkçe karakterleri (ı, ş, ç, ö, ğ, ü) ve
# sembolleri (✗, ! vb.) kodlayamıyor; konsolu UTF-8'a zorlayıp çökmeyi engelle.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

KOK = pathlib.Path(__file__).resolve().parent.parent
# Geode arayüzü çevirileri
GIRDI_GEC = [KOK / "glossary.tsv", KOK / "ceviriler" / "ceviri-tablosu.tsv"]
CIKTI_GEC = KOK / "src" / "translations.generated.hpp"

# Oyunun kendi menüleri (vanilla) çevirileri
GIRDI_VAN = [KOK / "ceviriler" / "vanilya-tablosu.tsv"]
CIKTI_VAN = KOK / "src" / "vanilla.generated.hpp"

# Çeviri yapılmayacak (teknik) metinler — İngilizce kalması gerekenler
KORUNACAK = {"Geode", "Geometry Dash", "Discord", "Modtober", "GitHub", "GD"}

def oku(yol):
    kayitlar = []
    if not yol.exists():
        return kayitlar
    with open(yol, encoding="utf-8") as f:
        okuyucu = csv.DictReader(f, delimiter="\t")
        for satir in okuyucu:
            en = (satir.get("EN") or satir.get("msgid") or "").strip()
            tr = (satir.get("TR") or satir.get("msgstr") or "").strip()
            durum = (satir.get("durum") or "").strip().lower()
            if not en or not tr:
                continue
            if durum and durum not in ("hazir", "hazır", "ok", "done"):
                continue
            kayitlar.append((en, tr, str(yol.name)))
    return kayitlar

def yer_tutucular(metin):
    return sorted(re.findall(r"\{\{?[^{}]*\}?\}", metin))

def etiketler(metin):
    return sorted(re.findall(r"</?c[a-z]?>", metin))

def denetle(kayitlar):
    hatalar, uyarilar = [], []
    gorulen = {}
    for en, tr, dosya in kayitlar:
        if en in gorulen and gorulen[en] != tr:
            uyarilar.append(f"ÇAKIŞMA: '{en}' iki farklı çeviriye sahip ({dosya})")
        gorulen[en] = tr

        # yer tutucular korunmuş mu ({}, {0}, {:.100} ...)
        if yer_tutucular(en) != yer_tutucular(tr):
            hatalar.append(f"YER TUTUCU: {en!r} -> {tr!r}  ({yer_tutucular(en)} != {yer_tutucular(tr)})")

        # renk etiketleri korunmuş mu
        if sorted(etiketler(en)) != sorted(etiketler(tr)):
            hatalar.append(f"ETİKET:     {en!r} -> {tr!r}  ({etiketler(en)} != {etiketler(tr)})")

        # kaçış dizileri (\n) korunmuş mu
        if en.count("\\n") != tr.count("\\n"):
            uyarilar.append(f"\\n SAYISI: {en!r} -> {tr!r}")

        # uzunluk kontrolü: bitmap font dar alanlarda taşabilir
        if len(tr) > len(en) * 2 + 12:
            uyarilar.append(f"UZUN:     {en!r} ({len(en)}) -> {tr!r} ({len(tr)}) — butona sığmayabilir")

    return hatalar, uyarilar

def kacisla(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')

def uret(kayitlar, ad="g_translations", kaynak_adi="glossary.tsv + ceviriler/ceviri-tablosu.tsv"):
    satirlar = [
        "// OTOMATİK ÜRETİLDİ — elle düzenlemeyin.",
        f"// Kaynak: {kaynak_adi}",
        "// Yeniden üretmek için: python3 arac/ceviri-olustur.py",
        "#pragma once",
        "#include <unordered_map>",
        "#include <string>",
        "",
        f"static std::unordered_map<std::string, std::string> const {ad} = {{",
    ]
    for en, tr, _ in sorted(kayitlar):
        satirlar.append(f'    {{"{kacisla(en)}", "{kacisla(tr)}"}},')
    satirlar += ["};", ""]
    return "\n".join(satirlar)

def tekillestir(kayitlar):
    tekil = {}
    for en, tr, d in kayitlar:
        tekil.setdefault(en, (en, tr, d))
    return list(tekil.values())


def main():
    sadece_kontrol = "--kontrol" in sys.argv

    geode_kayit = tekillestir(sum((oku(y) for y in GIRDI_GEC), []))
    vanilya_kayit = tekillestir(sum((oku(y) for y in GIRDI_VAN), []))

    kayitlar = geode_kayit + vanilya_kayit
    hatalar, uyarilar = denetle(kayitlar)

    print(f"Geode arayüzü: {len(geode_kayit)} çeviri")
    print(f"Oyun menüleri : {len(vanilya_kayit)} çeviri")
    print(f"Toplam        : {len(kayitlar)}")
    if hatalar:
        print(f"\n== {len(hatalar)} HATA (düzeltmeden derleme) ==")
        for h in hatalar:
            print("  ✗", h)
    if uyarilar:
        print(f"\n== {len(uyarilar)} UYARI ==")
        for u in uyarilar:
            print("  !", u)

    if sadece_kontrol:
        return 1 if hatalar else 0

    CIKTI_GEC.parent.mkdir(parents=True, exist_ok=True)
    CIKTI_GEC.write_text(uret(geode_kayit, "g_geode"), encoding="utf-8")
    CIKTI_VAN.write_text(
        uret(vanilya_kayit, "g_vanilya", "ceviriler/vanilya-tablosu.tsv"), encoding="utf-8"
    )
    print(f"\nYazıldı: {CIKTI_GEC.relative_to(KOK)}  ({len(geode_kayit)} kayıt)")
    print(f"Yazıldı: {CIKTI_VAN.relative_to(KOK)}  ({len(vanilya_kayit)} kayıt)")
    return 1 if hatalar else 0

if __name__ == "__main__":
    sys.exit(main())
