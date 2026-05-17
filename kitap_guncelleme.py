import json #Kitap listeni bir metin dosyasına yazar, programı tekrar açtığında oradan geri okur
import os#Bilgisayardaki dosyalarla ilgili işlemler yapmamızı sağlar
from dataclasses import dataclass, asdict
from tkinter import messagebox
from typing import List#Sadece liste değil kitap listeleri olduğunu belirtmek için kullanılır

@dataclass
class Kitap:#Kitap Bilgilerini tutan sınıf
    isbn: str           #Kitap numarası tc gibi benzersiz olmalı
    ad: str            
    yazar: str              
    stok: int           
    konum: str          
#Dosya işlemleri
DOSYA = os.path.join("veri", "kitaplar.json")#Kitap bilgilerini tutan dosyanın yolu pc hangi işletim sistemini kullanırsa kullansın doğru şekilde oluşturulmasını sağlar

def kitaplari_yukle() -> List[Kitap]:
    if not os.path.exists(DOSYA):#Dosya yoksa boş liste döndürür, böylece program ilk kez çalıştırıldığında hata olmaz
        return []
    with open(DOSYA, "r", encoding="utf-8") as f:#With kullanma sebebi dosya işlemi bittikten sonra dosyanın otomatik olarak kapanmasını sağlar
        veri = json.load(f)
    return [Kitap(**k) for k in veri]

def kitaplari_kaydet(liste: List[Kitap]):
    with open(DOSYA, "w", encoding="utf-8") as f:
        json.dump([asdict(k) for k in liste], f,
                  ensure_ascii=False, indent=2)#Kitap nesnelerini sözlük formatına çevirir ve json dosyasına yazar// Veriyi 2 boşluk girintili yazar
def kitap_ekle(isbn, ad, yazar, stok, konum):
    """Yeni kitap ekler. Aynı ISBN varsa reddeder."""
    kitaplar = kitaplari_yukle()

    for k in kitaplar:
        if k.isbn == isbn:
            messagebox.showerror("Hata", "Bu ISBN zaten kayıtlı.")
            return 0


    while True:
        try:
            stok = int(stok)
            if stok >= 0:
                break
            messagebox.showerror("Hata", "Stok negatif olamaz.")
            return 0
        except ValueError:
           messagebox.showerror("Hata", "Stok miktarı geçerli bir sayı olmalıdır.")
           return 0
    


    yeni = Kitap(isbn, ad, yazar, stok, konum)
    kitaplar.append(yeni)
    kitaplari_kaydet(kitaplar)
    messagebox.showinfo("Bilgi", f"'{ad}' kitabı başarıyla eklendi.")


def stok_guncelle():
    """Mevcut bir kitabın stok miktarını günceller."""
    print("\n--- Stok Güncelle ---")
    isbn = input("Güncellenecek kitabın ISBN'i: ").strip()
    kitaplar = kitaplari_yukle()

    for k in kitaplar:
        if k.isbn == isbn:
            print(f"  Kitap      : {k.ad}")
            print(f"  Mevcut stok: {k.stok}")
            while True:
                try:
                    yeni_stok = int(input("Yeni stok: ").strip())
                    if yeni_stok >= 0:
                        break
                    print("  Stok negatif olamaz.")
                except ValueError:
                    print("  Lütfen geçerli bir sayı girin.")
            k.stok = yeni_stok
            kitaplari_kaydet(kitaplar)
            print(f"✓ Stok güncellendi → {yeni_stok}")
            return

    print("✗ Kitap bulunamadı.")