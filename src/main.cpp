// Geode Türkçe Yerelleştirme — runtime çevirici (v0.2)
//
// İKİ KATMAN
//   1) Geode mod menüsü  → src/translations.generated.hpp  (g_geode)
//   2) Oyunun kendi menüleri (ayarlar, hesap, profil...) → src/vanilla.generated.hpp (g_vanilya)
//
// NEDEN BÖYLE?
//   GD'nin menü metinleri C++ içine gömülü ve çoğu CCLabelBMFont ile çiziliyor.
//   Vanilla çeviri yalnızca GlobalID (node ID) modu açıkken yapılır; böylece
//   kullanıcının yazdığı seviye adları, yorumlar, kullanıcı adları BOZULMAZ.
//
// SÖZLÜKLER OTOMATİK ÜRETİLİR — elle düzenlemeyin!
//   ceviriler/ceviri-tablosu.tsv  (Geode arayüzü)
//   ceviriler/vanilya-tablosu.tsv (oyun menüleri)
//   Üretim: python3 arac/ceviri-olustur.py

#include <Geode/Geode.hpp>
#include <Geode/modify/CCScene.hpp>
#include <Geode/modify/MenuLayer.hpp>
#include <Geode/modify/GlobalID.hpp>
#include <Geode/binding/FLAlertLayer.hpp>
#include <Geode/binding/GlobalID.hpp>
#include <cocos2d.h>
#include <string>

#include "translations.generated.hpp"
#include "vanilla.generated.hpp"

using namespace geode::prelude;

namespace {

constexpr float TARAMA_ARALIGI = 0.4f;
constexpr int   TARAMA_SAYISI  = 8;

// ---------------------------------------------------------------
// Sözlük arama yardımcıları
// ---------------------------------------------------------------

// Metnin içindeki <cy>...</c> renk etiketlerini KORUYARAK sadece düz metni çevirir.
template <class Harita>
bool cevirEtiketli(Harita const& harita, std::string const& src, std::string& out) {
    std::string sonuc;
    sonuc.reserve(src.size() + 16);
    bool degisti = false;

    size_t i = 0;
    while (i < src.size()) {
        if (src[i] == '<') {
            size_t son = src.find('>', i);
            if (son == std::string::npos) { sonuc.append(src, i, std::string::npos); break; }
            sonuc.append(src, i, son - i + 1);
            i = son + 1;
            continue;
        }
        size_t sonraki = src.find('<', i);
        std::string parca = src.substr(
            i, sonraki == std::string::npos ? std::string::npos : sonraki - i
        );

        auto it = harita.find(parca);
        if (it != harita.end()) { sonuc += it->second; degisti = true; }
        else sonuc += parca;

        if (sonraki == std::string::npos) break;
        i = sonraki;
    }

    if (!degisti) return false;
    out = sonuc;
    return true;
}

// birebir → etiketli sırasıyla arar. Bulamazsa false döner.
template <class Harita>
bool cevir(Harita const& harita, std::string const& src, std::string& out) {
    auto it = harita.find(src);
    if (it != harita.end()) { out = it->second; return !out.empty() && out != src; }
    return cevirEtiketli(harita, src, out);
}

// ---------------------------------------------------------------
// Yeni metin genişliği eski alana sığmıyorsa ölçeği küçült.
// (Türkçe İngilizce'den uzun → buton taşmalarını engeller.)
// ---------------------------------------------------------------
void sigdir(cocos2d::CCNode* node, float eskiGenislik, float yeniGenislik) {
    if (eskiGenislik <= 1.f || yeniGenislik <= eskiGenislik) return;
    float oran = eskiGenislik / yeniGenislik;
    node->setScaleX(node->getScaleX() * oran);
}

// ---------------------------------------------------------------
// Sözlüğü yaz. geriDondur=true ise çeviriyi geri alır (GlobalID kapanınca).
// ---------------------------------------------------------------
bool uygula(cocos2d::CCNode* node, std::string& ilkMetin, bool geriDondur) {
    auto* bm = typeinfo_cast<cocos2d::CCLabelBMFont*>(node);
    cocos2d::CCLabelTTF* ttf = nullptr;
#if defined(GEODE_IS_WINDOWS) || defined(GEODE_IS_MACOS) || defined(GEODE_IS_IOS)
    if (!bm) ttf = typeinfo_cast<cocos2d::CCLabelTTF*>(node);
#endif
    if (!bm && !ttf) return false;

    char const* mevcut = bm ? bm->getString() : ttf->getString();
    if (!mevcut || !*mevcut) return false;

    std::string src(mevcut);
    if (ilkMetin.empty()) ilkMetin = src;

    std::string hedef;
    if (geriDondur) {
        hedef = ilkMetin;                       // orijinal İngilizceye dön
    }
    else {
        // 1) Geode arayüzü sözlüğü
        if (!cevir(g_geode, src, hedef)) {
            // 2) Vanilla sözlüğü (yalnızca GlobalID açıksa)
            if (!Mod::get()->getSettingValue<bool>("vanilla-ceviri")) return false;
            if (!GlobalID::getGlobalIDEnabled()) return false;
            if (!cevir(g_vanilya, src, hedef)) return false;
        }
    }

    if (hedef.empty() || hedef == src) return false;

    float eskiGen = node->getContentSize().width;
    if (bm) {
        bm->setString(hedef.c_str(), true);      // true: label'ı yeniden kur
        sigdir(bm, eskiGen, bm->getContentSize().width);
    }
#if defined(GEODE_IS_WINDOWS) || defined(GEODE_IS_MACOS) || defined(GEODE_IS_IOS)
    else if (ttf) {
        ttf->setString(hedef.c_str());
        sigdir(ttf, eskiGen, ttf->getContentSize().width);
    }
#endif
    return true;
}

// Sahne ağacını özyinelemeli tara.
void tara(cocos2d::CCNode* node) {
    if (!node) return;

    // Çevrilen ilk metni node üzerinde saklıyoruz: kapatınca geri dönebilmek için.
    auto* veri = node->getUserObject();
    std::string ilkMetin;
    if (veri && typeinfo_cast<cocos2d::CCString*>(veri)) {
        ilkMetin = static_cast<cocos2d::CCString*>(veri)->getCString();
    }

    uygula(node, ilkMetin, false);

    if (!ilkMetin.empty()) {
        if (veri) static_cast<cocos2d::CCString*>(veri)->setString(ilkMetin.c_str());
        else node->setUserObject(cocos2d::CCString::createWithFormat("%s", ilkMetin.c_str()));
    }

    if (auto cocuklar = node->getChildren()) {
        for (unsigned int i = 0; i < cocuklar->count(); ++i) {
            tara(static_cast<cocos2d::CCNode*>(cocuklar->objectAtIndex(i)));
        }
    }
}

// GlobalID kapanınca yazıları İngilizceye geri al.
void geriAl(cocos2d::CCNode* node) {
    if (!node) return;
    auto* veri = node->getUserObject();
    if (veri && typeinfo_cast<cocos2d::CCString*>(veri)) {
        std::string ilk = static_cast<cocos2d::CCString*>(veri)->getCString();
        std::string simdiki;
        if (cocos2d::CCLabelBMFont* bm = typeinfo_cast<cocos2d::CCLabelBMFont*>(node)) {
            simdiki = bm->getString();
            if (!ilk.empty() && simdiki != ilk) bm->setString(ilk.c_str(), true);
        }
    }
    if (auto cocuklar = node->getChildren()) {
        for (unsigned int i = 0; i < cocuklar->count(); ++i) {
            geriAl(static_cast<cocos2d::CCNode*>(cocuklar->objectAtIndex(i)));
        }
    }
}

// cocos2d-x 2.x action callback'i için basit hedef nesnesi.
class Tarayici : public cocos2d::CCObject {
public:
    cocos2d::CCNode* hedef = nullptr;
    static Tarayici* create(cocos2d::CCNode* h) {
        auto* n = new Tarayici();
        n->hedef = h;
        n->autorelease();
        return n;
    }
    void calis() { tara(hedef); }
};

class GeriAlma : public cocos2d::CCObject {
public:
    cocos2d::CCNode* hedef = nullptr;
    static GeriAlma* create(cocos2d::CCNode* h) {
        auto* n = new GeriAlma();
        n->hedef = h;
        n->autorelease();
        return n;
    }
    void calis() { geriAl(hedef); }
};

// ---------------------------------------------------------------
// Font kontrolü: bigFont.fnt içinde ğ/ş/İ/ı glifleri var mı?
// Türkçe çeviri yapıp bu glifler yoksa oyunda "kutu" görünür.
// Kullanıcıya bir kez, tıklanabilir bir uyarı gösteriyoruz.
// ---------------------------------------------------------------
bool fontTurkceDestekliyor() {
    static int onbellek = -1;                 // -1: bilinmiyor, 0: yok, 1: var
    if (onbellek != -1) return onbellek == 1;

    auto* bm = cocos2d::CCLabelBMFont::create("sSgGiI", "bigFont.fnt");
    if (!bm) { onbellek = 0; return false; }

    // Atlas eksik glif yerine boş/beyaz kutu koyar → genişlik beklenenden farklı olur.
    char const* metin = bm->getString();
    bool var = metin && std::string(metin) == "sSgGiI";
    onbellek = var ? 1 : 0;
    return var;
}

void fontUyarisiGoster() {
    if (!Mod::get()->getSettingValue<bool>("font-hatirlat")) return;
    if (fontTurkceDestekliyor()) return;

    FLAlertLayer::create(
        "Türkçe Font Gerekli",
        "Türkçe karakterler (<cy>ğ ş İ ı</c>) oyunun varsayılan fontunda yok.\n\n"
        "Bu yüzden bazı harfler <cr>kutu</c> olarak görünebilir.\n\n"
        "<cg>Çözüm:</c> Texture Loader ile \"Türkçe Font Paketi\"ni kur "
        "(bigFont.fnt + goldFont.fnt).",
        "Tamam"
    )->show();
}

} // namespace

// Ana menüye girildiğinde bir kez font kontrolü yap.
class $modify(TRMenuLayer, MenuLayer) {
    bool init() {
        if (!MenuLayer::init()) return false;
        this->runAction(cocos2d::CCSequence::create(
            cocos2d::CCDelayTime::create(1.0f),
            cocos2d::CCCallFunc::create(this, callfunc_selector(TRMenuLayer::fontKontrol)),
            nullptr
        ));
        return true;
    }

    void fontKontrol() { fontUyarisiGoster(); }
};

// Her sahnede ~3 saniye boyunca tarama yap (menü içeriği gecikmeli geliyor).
class $modify(TRScene, cocos2d::CCScene) {
    bool init() {
        if (!cocos2d::CCScene::init()) return false;

        auto adim = cocos2d::CCSequence::create(
            cocos2d::CCDelayTime::create(TARAMA_ARALIGI),
            cocos2d::CCCallFunc::create(Tarayici::create(this), callfunc_selector(Tarayici::calis)),
            nullptr
        );
        this->runAction(cocos2d::CCRepeat::create(adim, TARAMA_SAYISI));
        return true;
    }
};

// GlobalID ayarı kapatılırsa (kullanıcı isimleri karışmasın diye) yazıları geri al.
class $modify(TRGlobalIDHook, GlobalID) {
    static void setGlobalIDEnabled(bool enabled) {
        GlobalID::setGlobalIDEnabled(enabled);
        if (!enabled) {
            if (auto sahne = cocos2d::CCDirector::get()->getRunningScene()) {
                sahne->runAction(cocos2d::CCSequence::create(
                    cocos2d::CCDelayTime::create(0.1f),
                    cocos2d::CCCallFunc::create(
                        GeriAlma::create(sahne), callfunc_selector(GeriAlma::calis)
                    ),
                    nullptr
                ));
            }
        }
    }
};
