import json
import hashlib # şifreleme için
import os
from dataclasses import dataclass, asdict 
from typing import Optional
@dataclass # c deki struct gibi, sadece veri tutar
class Kullanici:
    kullanici_adi: str
    sifre_hash: str      #düz metin saklanmaz şifreleme için kullandğmz hali saklanır ve bu hal geriye çevirlemez
    rol: str             # yönetici ogrenci gibi
    ad_soyad: str
    ogrenci_no: str = ""

DOSYA = os.path.join("veri", "kullanicilar.json") # tüm sistemlerde çalışması için os.path.join kullanılır

def kullanicilari_yukle():
    if not os.path.exists(DOSYA):# dosya yoksa boş liste döndür
        return []# henüz kullanıcı yok anlamına gelir
    with open(DOSYA, "r", encoding="utf-8") as f:#utf-8 ile açılır türkçe karakterler için
        veri = json.load(f)#python nesnesine dönüştürür
    return [Kullanici(**u) for u in veri]# verileri düzenleyen kısım **u ile sözlükten nesne oluşturur

def kullanicilari_kaydet(liste):
    with open(DOSYA, "w", encoding="utf-8") as f:
        json.dump([asdict(u) for u in liste], f,#@datasclass ile oluşturulan nesneleri sözlüğe çevirir
                  ensure_ascii=False, indent=2)#Türkçe karakterleri bozmaz düzgün kaydeder
# ── Şifreleme ve Doğrulama
def sifrele(sifre: str) -> str:
    return hashlib.sha256(sifre.encode("utf-8")).hexdigest()#sha256 metin değil byte alır bu yüzden encode ile byte'a çeviririz ve hexdigest ile okunabilir hale getiririz

def sifre_dogru_mu(girilen: str, kayitli_hash: str) -> bool:
    return sifrele(girilen) == kayitli_hash
# ── YETKİ KONTROLÜ
def yetki_var_mi(kullanici: Kullanici, gereken_rol: str) -> bool:
    """ Yönetici her şeyi yapabilir"""
    hiyerarsi = {
        "yonetici": 3,#Her rolün bir sayısı var en yüksek sayı yöneticide yani en üst yönetici
        "personel": 2,
        "ogrenci":  1
    }
    kullanici_seviye = hiyerarsi.get(kullanici.rol, 0)#.get ile rolün seviyesini alırız eğer rol tanımlı değilse 0 döner
    gereken_seviye   = hiyerarsi.get(gereken_rol, 99)
    return kullanici_seviye >= gereken_seviye#kullanıcının sayısı gerekenden büyükse true döner
# ── İLK KURULUM
def sistem_hazirla():
    os.makedirs("veri", exist_ok=True)# veri klasörünü oluşturur eğer zaten varsa hata vermez
    if not kullanicilari_yukle():#hiç kullanıcı yoksa ilk çalışmada buraya geliriz
        admin = Kullanici(#ilk admin oluşturulur
            kullanici_adi = "admin",
            sifre_hash    = sifrele("admin123"),
            rol           = "yonetici",
            ad_soyad      = "Sistem Yöneticisi"
        )
        kullanicilari_kaydet([admin])
        print("✓ İlk admin oluşturuldu. Şifre: admin123")

# ── GİRİŞ
def giris_yap() -> Optional[Kullanici]:
    print("\n=== KÜTÜPHANE SİSTEMİ ===")
    k_adi = input("Kullanıcı adı: ").strip()#kullanıcı adını alır ve baştaki sondaki boşlukları temizler
    sifre = input("Şifre        : ").strip()#şifreyi alır ve baştaki sondaki boşlukları temizler

    for u in kullanicilari_yukle():#kullanıcıları yükler ve her kullanıcı için kontrol eder
        if u.kullanici_adi == k_adi and sifre_dogru_mu(sifre, u.sifre_hash):
            print(f"\n✓ Hoş geldiniz, {u.ad_soyad}! [{u.rol}]")
            return u#giriş başarılıysa kullanıcı nesnesini döndürür

    print("✗ Hatalı kullanıcı adı veya şifre.")#hangisinin yanlış olduğunu söylemeyiz güvenlik için
    return None#giriş başarısızsa None döner

# ── TEST
if __name__ == "__main__":
    sistem_hazirla()
    kullanici = giris_yap()

    if kullanici:
        # Yetki testi
        if yetki_var_mi(kullanici, "yonetici"):
            print("→ Yönetici paneline erişebilirsiniz.")
        elif yetki_var_mi(kullanici, "personel"):
            print("→ Personel paneline erişebilirsiniz.")
        else:
            print("→ Öğrenci paneline erişebilirsiniz.")