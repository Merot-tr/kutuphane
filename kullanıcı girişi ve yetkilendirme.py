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

def sifrele(sifre: str) -> str:
    return hashlib.sha256(sifre.encode("utf-8")).hexdigest()
print(sifrele("admin123"))   # Hash çıktısını gör
print(sifrele("admin123"))   # Aynı hash çıktığını gör
print(sifrele("Admin123"))   # Tamamen farklı hash!