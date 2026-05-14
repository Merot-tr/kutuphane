import os
import json
from dataclasses import dataclass, asdict
from typing import List

# IP1'deki Kullanici ve fonksiyonları buraya kopyala
@dataclass
class Kullanici:
    kullanici_adi: str
    sifre_hash: str
    rol: str
    ad_soyad: str
    ogrenci_no: str = ""

import hashlib
DOSYA = os.path.join("veri", "kullanicilar.json")#veriyi klasöründe kullanicilar.json dosyasını oluşturur

def kullanicilari_yukle():
    if not os.path.exists(DOSYA):#dosya yoksa boş liste döndürür
        return []
    with open(DOSYA, "r", encoding="utf-8") as f:
        veri = json.load(f)#json dosyasındaki veriyi okuyup python listesine çevirir
    return [Kullanici(**u) for u in veri]#sözlük verilerini kullanıcı nesnesine çevirir

def kullanicilari_kaydet(liste):
    with open(DOSYA, "w", encoding="utf-8") as f:#kullanıcı listesini json dosyasına kaydeder
        json.dump([asdict(u) for u in liste], f,
                  ensure_ascii=False, indent=2)
#Kullanıcı oluşturma fonksiyonu
def sifrele(sifre: str) -> str:
    return hashlib.sha256(sifre.encode("utf-8")).hexdigest()
def kullanici_olustur():
    print("\n--- Kullanıcı Oluştur ---")
    kullanicilar = kullanicilari_yukle()

    k_adi = input("Kullanıcı Adı : ").strip()

    # Aynı kullanıcı adı var mı?
    for u in kullanicilar:
        if u.kullanici_adi == k_adi:
            print("✗ Bu kullanıcı adı zaten alınmış!")#kullanıcı adı zaten varsa hata mesajı verir ve fonksiyondan çıkar
            return

    sifre    = input("Şifre         : ").strip()
    ad_soyad = input("Ad Soyad      : ").strip()

    print("Rol seçin:")
    print("  1. Yönetici")
    print("  2. Personel")
    print("  3. Öğrenci")
    secim = input("Seçim: ").strip()

    roller = {"1": "yonetici", "2": "personel", "3": "ogrenci"}
    rol = roller.get(secim, "ogrenci")  # geçersiz seçimde öğrenci ata

    ogr_no = ""#seçim öğrenci ise öğrenci numarası iste, değilse boş bırak
    if rol == "ogrenci":
        ogr_no = input("Öğrenci No : ").strip()

    yeni = Kullanici(k_adi, sifrele(sifre), rol, ad_soyad, ogr_no)#yeni kullanıcı nesnesi oluşturur
    kullanicilar.append(yeni)
    kullanicilari_kaydet(kullanicilar)
    print(f"✓ '{k_adi}' kullanıcısı oluşturuldu [{rol}]")
#Kullanıcı silme fonksiyonu
def kullanici_sil(aktif_kullanici):
    print("\n--- Kullanıcı Sil ---")
    kullanicilar = kullanicilari_yukle()

    k_adi = input("Silinecek kullanıcı adı: ").strip()

    # Kendini silemez
    if k_adi == aktif_kullanici.kullanici_adi:
        print("✗ Kendi hesabınızı silemezsiniz!")
        return

    yeni_liste = [u for u in kullanicilar if u.kullanici_adi != k_adi]#silinen kullanıcı hariç yeni liste oluşturur

    if len(yeni_liste) == len(kullanicilar):
        print("✗ Kullanıcı bulunamadı.")
        return#listenin boyutu değişmediyse kullanıcı bulunamamıştır

    kullanicilari_kaydet(yeni_liste)
    print(f"✓ '{k_adi}' silindi.")
#Kullanıcıları listeleme fonksiyonu
def kullanicilari_listele():
    print("\n--- Kullanıcı Listesi ---")
    kullanicilar = kullanicilari_yukle()

    if not kullanicilar:
        print("Henüz kullanıcı yok.")
        return

    print(f"\n{'Kullanıcı Adı':<20} {'Ad Soyad':<25} {'Rol':<12} {'Öğrenci No'}")
    print("-" * 65)
    for u in kullanicilar:
        print(f"{u.kullanici_adi:<20} {u.ad_soyad:<25} {u.rol:<12} {u.ogrenci_no}")
if __name__ == "__main__":
    os.makedirs("veri", exist_ok=True)

    while True:
        print("\n1. Kullanıcı Oluştur")
        print("2. Kullanıcı Sil")
        print("3. Kullanıcıları Listele")
        print("0. Çıkış")
        secim = input("Seçim: ").strip()

        if secim == "1":
            kullanici_olustur()
        elif secim == "2":
            # Test için sahte aktif kullanıcı
            sahte = Kullanici("admin", "", "yonetici", "Admin")
            kullanici_sil(sahte)
        elif secim == "3":
            kullanicilari_listele()
        elif secim == "0":
            break