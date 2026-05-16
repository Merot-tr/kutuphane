import os
import json
import datetime
import hashlib
from dataclasses import dataclass, asdict
from typing import List

@dataclass
class OduncKaydi:
    kayit_id: str
    isbn: str
    kullanici_adi: str
    odunc_tarihi: str
    iade_tarihi: str
    geri_donus_tarihi: str  # boşsa henüz iade edilmedi

DOSYA = os.path.join("veri", "odunc_kayitlari.json")
KITAP_DOSYA = os.path.join("veri", "kitaplar.json")

def kayit_id_olustur():
    n = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    return hashlib.md5(n.encode()).hexdigest()[:10].upper()

def oduncleri_yukle():
    if not os.path.exists(DOSYA):
        return []
    with open(DOSYA, "r", encoding="utf-8") as f:
        return [OduncKaydi(**o) for o in json.load(f)]

def oduncleri_kaydet(liste):
    with open(DOSYA, "w", encoding="utf-8") as f:
        json.dump([asdict(o) for o in liste], f,
                  ensure_ascii=False, indent=2)

def kitap_stok_guncelle(isbn, miktar):
    # stok düşür veya artır
    if not os.path.exists(KITAP_DOSYA):
        return
    with open(KITAP_DOSYA, "r", encoding="utf-8") as f:
        kitaplar = json.load(f)
    for k in kitaplar:
        if k["isbn"] == isbn:
            k["stok"] += miktar
            break
    with open(KITAP_DOSYA, "w", encoding="utf-8") as f:
        json.dump(kitaplar, f, ensure_ascii=False, indent=2)

def odunc_al():
    print("\n--- Kitap Ödünç Al ---")
    isbn = input("ISBN: ").strip()
    kullanici = input("Kullanıcı Adı: ").strip()

    # Stok kontrolü
    if not os.path.exists(KITAP_DOSYA):
        print("✗ Kitap bulunamadı.")
        return
    with open(KITAP_DOSYA, "r", encoding="utf-8") as f:
        kitaplar = json.load(f)
    kitap = next((k for k in kitaplar if k["isbn"] == isbn), None)
    if not kitap:
        print("✗ Kitap bulunamadı.")
        return
    if kitap["stok"] <= 0:
        print("✗ Stokta kitap kalmamış.")
        return

    # Zaten ödünçte mi?
    oduncler = oduncleri_yukle()
    for o in oduncler:
        if o.isbn == isbn and o.kullanici_adi == kullanici and not o.geri_donus_tarihi:
            print("✗ Bu kitap zaten bu kullanıcıda!")
            return

    # Kayıt oluştur
    bugun = datetime.date.today()
    iade = bugun + datetime.timedelta(days=14)  # 14 gün süre
    kayit = OduncKaydi(
        kayit_id=kayit_id_olustur(),
        isbn=isbn,
        kullanici_adi=kullanici,
        odunc_tarihi=str(bugun),
        iade_tarihi=str(iade),
        geri_donus_tarihi=""
    )
    oduncler.append(kayit)
    oduncleri_kaydet(oduncler)
    kitap_stok_guncelle(isbn, -1)  # stok 1 azalt
    print(f"✓ Ödünç alındı! İade tarihi: {iade} | Kayıt ID: {kayit.kayit_id}")

def iade_et():
    print("\n--- Kitap İade Et ---")
    kayit_id = input("Kayıt ID: ").strip().upper()
    oduncler = oduncleri_yukle()

    kayit = next((o for o in oduncler if o.kayit_id == kayit_id), None)
    if not kayit:
        print("✗ Kayıt bulunamadı.")
        return
    if kayit.geri_donus_tarihi:
        print("✗ Bu kitap zaten iade edilmiş.")
        return

    bugun = datetime.date.today()
    kayit.geri_donus_tarihi = str(bugun)
    oduncleri_kaydet(oduncler)
    kitap_stok_guncelle(kayit.isbn, +1)  # stok 1 artır

    iade = datetime.date.fromisoformat(kayit.iade_tarihi)
    if bugun > iade:
        gun = (bugun - iade).days
        print(f"⚠ {gun} gün geç iade edildi!")
    print("✓ İade alındı!")

def odunc_listele():
    print("\n--- Ödünç Kayıtları ---")
    oduncler = oduncleri_yukle()
    if not oduncler:
        print("Henüz ödünç kaydı yok.")
        return
    bugun = datetime.date.today()
    print(f"\n{'Kayıt ID':<12} {'ISBN':<15} {'Kullanıcı':<15} {'İade Son':<12} {'Durum'}")
    print("-" * 65)
    for o in oduncler:
        if o.geri_donus_tarihi:
            durum = "İade Edildi"
        else:
            iade = datetime.date.fromisoformat(o.iade_tarihi)
            durum = f"GECİKMİŞ {(bugun-iade).days}g" if bugun > iade else "Aktif"
        print(f"{o.kayit_id:<12} {o.isbn:<15} {o.kullanici_adi:<15} {o.iade_tarihi:<12} {durum}")

if __name__ == "__main__":
    os.makedirs("veri", exist_ok=True)
    while True:
        print("\n1. Kitap Ödünç Al")
        print("2. Kitap İade Et")
        print("3. Ödünç Listesi")
        print("0. Çıkış")
        secim = input("Seçim: ").strip()
        if secim == "1":
            odunc_al()
        elif secim == "2":
            iade_et()
        elif secim == "3":
            odunc_listele()
        elif secim == "0":
            break
        else:
            print("Geçersiz seçim.")