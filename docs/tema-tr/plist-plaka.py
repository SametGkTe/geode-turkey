#!/usr/bin/env python3
"""
plist-plaka.py — Cocos2d spritesheet (.plist) içinden TEK bir kareyi
ayrı PNG olarak çıkarır.

NEDEN GEREKLİ?
  Geometry Dash'te logo gibi görseller tek PNG değil, bir SPRITESHEET içinde
  duruyor (örnek: "GJ_logo_001.png" → GJ_LaunchSheet-hd.plist içinde).
  Bu yüzden mods/texture pack içine "GJ_logo_001.png" adında bir dosya koymak
  TEK BAŞINA işe yaramaz; dosya, plist'in adıyla aynı olmalı ve içinde o kare
  bulunmalı:
      GJ_LaunchSheet-hd.png   +   GJ_LaunchSheet-hd.plist
      GJ_LaunchSheet-uhd.png  +   GJ_LaunchSheet-uhd.plist
  Bu script orijinal plist'ten kare koordinatlarını okur, kaynak PNG'den kareyi
  keser ve doğru isimle kaydeder. Sonra üzerine kendi logonu çizersin.

KULLANIM
    # 1) Plist içindeki tüm kareleri listele
    python3 plist-plaka.py --liste GJ_LaunchSheet-hd.plist

    # 2) Tek kareyi çıkar (üzerine çizmek için şablon)
    python3 plist-plaka.py GJ_LaunchSheet-hd.plist GJ_LaunchSheet-hd.png \
        "GJ_logo_001.png" sablon/GJ_LaunchSheet-hd.png

    # 3) Tüm kareleri tek klasöre çıkar (spritesheet'i yeniden kurmak için)
    python3 plist-plaka.py --tumu GJ_LaunchSheet-hd.plist GJ_LaunchSheet-hd.png sablon/

GEREKSİNİM: Pillow  →  pip install pillow
"""

import sys, plistlib, pathlib, re


# ---------------- plist ayrıştırma (cocos2d format 2/3) ----------------

def _boyut(s):
    """'{1,2}' veya '{{0,0},{10,20}}' gibi dizeleri sayı listesine çevirir."""
    return [float(x) for x in re.findall(r"-?\d+\.?\d*", s or "")]


def kareleri_oku(plist_yolu):
    with open(plist_yolu, "rb") as f:
        veri = plistlib.load(f)

    kareler = {}
    for ad, k in veri.get("frames", {}).items():
        if "textureRect" in k:                       # format 3
            x, y, w, h = _boyut(k["textureRect"])
            kaynak = _boyut(k.get("spriteSourceSize", f"{{{w},{h}}}"))
            ofset = _boyut(k.get("spriteOffset", "{0,0}"))
            kayit = {
                "x": int(x), "y": int(y), "w": int(w), "h": int(h),
                "sw": int(kaynak[0]) if kaynak else int(w),
                "sh": int(kaynak[1]) if len(kaynak) > 1 else int(h),
                "ox": int(ofset[0]) if ofset else 0,
                "oy": int(ofset[1]) if len(ofset) > 1 else 0,
                "rotated": bool(k.get("textureRotated", False)),
            }
        elif "frame" in k:                           # format 2
            x, y, w, h = _boyut(k["frame"])
            kayit = {"x": int(x), "y": int(y), "w": int(w), "h": int(h),
                     "sw": int(w), "sh": int(h), "ox": 0, "oy": 0,
                     "rotated": bool(k.get("rotated", False))}
        else:
            continue
        kareler[ad] = kayit

    dosya_adi = veri.get("metadata", {}).get("realTextureFileName") \
                or veri.get("metadata", {}).get("textureFileName")
    return kareler, dosya_adi


# ---------------- kare kesme ----------------

def kare_kes(kaynak_img, kare):
    from PIL import Image

    x, y, w, h = kare["x"], kare["y"], kare["w"], kare["h"]
    kesit = kaynak_img.crop((x, y, x + w, y + h))

    if kare["rotated"]:
        kesit = kesit.transpose(Image.ROTATE_90)

    # Orijinal mantıksal boyut (şeffaf boşluklar) farklıysa tuvale ortala
    sw, sh = kare["sw"], kare["sh"]
    if (sw, sh) != kesit.size:
        tuval = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
        px = (sw - kesit.size[0]) // 2 + kare["ox"]
        py = (sh - kesit.size[1]) // 2 - kare["oy"]
        tuval.paste(kesit, (px, py), kesit)
        kesit = tuval
    return kesit


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 1

    mod = sys.argv[1]

    if mod == "--liste":
        kareler, dosya = kareleri_oku(sys.argv[2])
        print(f"{len(kareler)} kare (kaynak: {dosya}):")
        for ad, k in sorted(kareler.items()):
            print(f"  {ad:44s} {k['sw']}x{k['sh']}")
        return 0

    if mod == "--tumu":
        plist, png, cikti = sys.argv[2], sys.argv[3], sys.argv[4]
        from PIL import Image
        kareler, _ = kareleri_oku(plist)
        kaynak = Image.open(png).convert("RGBA")
        pathlib.Path(cikti).mkdir(parents=True, exist_ok=True)
        for ad, k in kareler.items():
            kare_kes(kaynak, k).save(pathlib.Path(cikti) / ad)
        print(f"{len(kareler)} kare çıkarıldı → {cikti}/")
        return 0

    if len(sys.argv) < 5:
        print(__doc__)
        return 1

    plist, png, kare_adi, cikti = sys.argv[1:5]
    from PIL import Image
    kareler, _ = kareleri_oku(plist)
    if kare_adi not in kareler:
        print(f"HATA: '{kare_adi}' plist içinde yok. --liste ile bak.")
        return 1
    kaynak = Image.open(png).convert("RGBA")
    kesit = kare_kes(kaynak, kareler[kare_adi])
    pathlib.Path(cikti).parent.mkdir(parents=True, exist_ok=True)
    kesit.save(cikti)
    print(f"Yazıldı: {cikti}  ({kesit.size[0]}x{kesit.size[1]})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
