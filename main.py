class Kullanici:
    def __init__(self, kullanici_adi, sifre, yetki="Uye"):
        self.kullanici_adi = kullanici_adi
        self.sifre = sifre  
        self.yetki = yetki

    def __str__(self):
        return f"{self.kullanici_adi}|{self.sifre}|{self.yetki}"

class Admin(Kullanici):
    def __init__(self, kullanici_adi, sifre):
        super().__init__(kullanici_adi, sifre, yetki="Admin")

class Mudur(Kullanici):
    def __init__(self, kullanici_adi, sifre):
        super().__init__(kullanici_adi, sifre, yetki="Mudur")

class Kitap:
    def __init__(self, kitap_adi, yazar, isbn, durum="Mevcut", kiralayan="Yok"):
        self.kitap_adi = kitap_adi
        self.yazar = yazar
        self.isbn = isbn
        self.durum = durum  
        self.kiralayan = kiralayan

    def __str__(self):
        return f"{self.kitap_adi}|{self.yazar}|{self.isbn}|{self.durum}|{self.kiralayan}"        

kullanicilar = [
    Admin("mehmet_admin", "12345"),
    Mudur("ayse_mudur", "qwerty"),
    Kullanici("ali_uye", "98765")
]


kitaplar = [
    Kitap("Sefiller", "Victor Hugo", "978123"),
    Kitap("Suç ve Ceza", "Dostoyevski", "978456"),
    Kitap("Python Programlama", "M. Elkoca", "978789", durum="Kirada", kiralayan="ali_uye")
]


def verileri_kaydet(dosya_adi, veri_listesi):
    with open(dosya_adi, "w", encoding="utf-8") as f:
        for veri in veri_listesi:
            f.write(str(veri) + "\n")


verileri_kaydet("kullanicilar.txt", kullanicilar)
verileri_kaydet("kitaplar.txt", kitaplar)

