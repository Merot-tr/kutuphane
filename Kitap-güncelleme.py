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