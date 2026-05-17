import os
import json
from dataclasses import dataclass, asdict
from typing import List

@dataclass
class Kitap:
    isbn: str
    ad: str
    yazar: str
    stok: int
    konum: str

DOSYA = os.path.join("veri", "kitaplar.json")

def kitaplari_yukle() -> List[Kitap]:
    if not os.path.exists(DOSYA):
        return []#dosya yoksa boş liste döndürür, böylece program ilk kez çalıştırıldığında hata olmaz
    with open(DOSYA, "r", encoding="utf-8") as f:#with kullanma sebebi dosya işlemi bittikten sonra dosyanın otomatik olarak kapanmasını sağlar
        veri = json.load(f)#python nesnesine dönüştürür
    return [Kitap(**k) for k in veri]#verileri düzenleyen kısım **k ile sözlükten nesne oluşturur
#arama fonksiyonu
def kitap_ara():
    print("\n--- Kitap Ara ---")
    print("1. Ada göre ara")
    print("2. Yazara göre ara")
    print("3. ISBN'ye göre ara")
    secim = input("Seçim: ").strip()

    aranan = input("Aranacak kelime: ").strip().lower()#aranacak kelimeyi küçük harfe çevirir

    kitaplar = kitaplari_yukle()

    # Hangi alana göre aranacak?
    if secim == "1":
        sonuclar = [k for k in kitaplar if aranan in k.ad.lower()]#in parçalı arama yapmamızı sağlar
    elif secim == "2":
        sonuclar = [k for k in kitaplar if aranan in k.yazar.lower()]
    elif secim == "3":
        sonuclar = [k for k in kitaplar if aranan in k.isbn.lower()]
    else:
        print("Geçersiz seçim.")
        return

    # Alfabetik sıralama
    sonuclar.sort(key=lambda k: k.ad.lower())

    if not sonuclar:
        print("✗ Sonuç bulunamadı.")
        return

    kitaplari_yazdir(sonuclar)
#listeleme fonksiyonu
def kitaplari_listele():
    print("\n--- Tüm Kitaplar ---")
    kitaplar = kitaplari_yukle()

    if not kitaplar:
        print("Henüz kitap yok.")
        return

    kitaplar.sort(key=lambda k: k.ad.lower())
    kitaplari_yazdir(kitaplar)
#tablo şeklinde yazdırma fonksiyonu
def kitaplari_yazdir(kitaplar: List[Kitap]):
    print(f"\n{len(kitaplar)} kitap bulundu:\n")
    print(f"{'ISBN':<15} {'Ad':<30} {'Yazar':<20} {'Stok':<6} {'Konum'}")
    print("-" * 80)
    for k in kitaplar:
        print(f"{k.isbn:<15} {k.ad[:29]:<30} {k.yazar[:19]:<20} {k.stok:<6} {k.konum}")
#test
if __name__ == "__main__":
    os.makedirs("veri", exist_ok=True)

    while True:
        print("\n1. Kitap Ara")
        print("2. Tüm Kitapları Listele")
        print("0. Çıkış")
        secim = input("Seçim: ").strip()

        if secim == "1":
            kitap_ara()
        elif secim == "2":
            kitaplari_listele()
        elif secim == "0":
            break
        else:
            print("Geçersiz seçim.")