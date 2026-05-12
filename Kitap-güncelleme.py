import json #Kitap listeni bir metin dosyasına yazar, programı tekrar açtığında oradan geri okur
import os#Bilgisayardaki dosyalarla ilgili işlemler yapmamızı sağlar
from dataclasses import dataclass, asdict
from typing import List#Sadece liste değil kitap listeleri olduğunu belirtmek için kullanılır

@dataclass
class Kitap:#Kitap Bilgilerini tutan sınıf
    isbn: str           #Kitap numarası tc gibi benzersiz olmalı
    ad: str            
    yazar: str         
    yayinevi: str        
    yayin_yili: int      
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
#Kitap ekleme fonksiyonu
def kitap_ekle():
    print("\n--- Kitap Ekle ---")
    kitaplar = kitaplari_yukle()  # mevcut kitapları getir
    isbn = input("ISBN: ").strip()
    # Aynı ISBN var mı kontrol et
    for k in kitaplar:
        if k.isbn == isbn:
            print("✗ Bu ISBN zaten kayıtlı!")
            return   # fonksiyondan çık, ekleme yapma
# Bilgileri al
    ad         = input("Kitap Adı  : ").strip()#strip() kullanma sebebi kullanıcı yanlışlıkla boşluk bıraktığında onu temizlemek için
    yazar      = input("Yazar      : ").strip()
    yayinevi   = input("Yayınevi   : ").strip()
    yayin_yili = int(input("Yayın Yılı : ").strip())
    stok       = int(input("Stok       : ").strip())
    konum      = input("Konum      : ").strip()
    # Yeni kitap nesnesi oluştur
    yeni_kitap = Kitap(isbn, ad, yazar, yayinevi,
                       yayin_yili, stok, konum)
# Listeye ekle ve kaydet
    kitaplar.append(yeni_kitap)
    kitaplari_kaydet(kitaplar)
    print(f"✓ '{ad}' eklendi!")
#Kitap güncelleme fonksiyonu
def kitap_guncelle():
    print("\n--- Kitap Güncelle ---")
    kitaplar = kitaplari_yukle()
    isbn = input("Güncellenecek ISBN: ").strip()
# ISBN'e göre kitabı bul
    kitap = None
    for k in kitaplar:
        if k.isbn == isbn:#Eğer kitap bulunduysa kitap değişkenine atar ve aramayı durdurur
            kitap = k
            break   # bulduk, aramayı durdur
    if kitap is None:
        print("✗ Kitap bulunamadı.")
        return
    print(f"Mevcut: {kitap.ad} | Stok: {kitap.stok}")
# Boş bırakılırsa eskisi kalır
    yeni_ad = input(f"Yeni Ad [{kitap.ad}]: ").strip()
    if yeni_ad:        # boş değilse güncelle
        kitap.ad = yeni_ad
    yeni_stok = input(f"Yeni Stok [{kitap.stok}]: ").strip()
    if yeni_stok:
        kitap.stok = int(yeni_stok)
    yeni_konum = input(f"Yeni Konum [{kitap.konum}]: ").strip()
    if yeni_konum:
        kitap.konum = yeni_konum
    kitaplari_kaydet(kitaplar)
    print("✓ Kitap güncellendi!")
#Kitap silme fonksiyonu
def kitap_sil():
    print("\n--- Kitap Sil ---")
    kitaplar = kitaplari_yukle()
    isbn = input("Silinecek ISBN: ").strip()
# Silinecek kitabı bul
    silinecek = None
    for k in kitaplar:
        if k.isbn == isbn:
            silinecek = k
            break
    if silinecek is None:
        print("✗ Kitap bulunamadı.")
        return
    # Onay al
    onay = input(f"'{silinecek.ad}' silinsin mi? (e/h): ").strip().lower()#Kullanıcıdan silme işlemi için onay alır e dışında başka bir harf girerse tekrar fonksiyonu döndürür
    if onay != "e":
        print("İptal edildi.")
        return
    # Listeden çıkar ve kaydet
    kitaplar = [k for k in kitaplar if k.isbn != isbn]#yeni bir liste yapar ve listeye silinicek olanı eklemez
    kitaplari_kaydet(kitaplar)
    print("✓ Kitap silindi.")
if __name__ == "__main__":
    os.makedirs("veri", exist_ok=True)
    while True:
        print("\n1. Ekle  2. Güncelle  3. Sil  0. Çıkış")
        secim = input("Seçim: ").strip()

        if secim == "1":
            kitap_ekle()
        elif secim == "2":
            kitap_guncelle()
        elif secim == "3":
            kitap_sil()
        elif secim == "0":
            break
        else:
            print("Geçersiz seçim.")