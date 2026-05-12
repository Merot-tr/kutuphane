import os
import sys
import kitap_guncelleme as kg
import kullanici_girisi_ve_yetkilendirme as ky

def menuyu_goster(kullanici):
    print(f"\n--- {kullanici.ad_soyad.upper()} ({kullanici.rol}) ---")
    print("1. Kitapları Listele (Sıralı)")
    print("2. Kitap Ara (İsim/ISBN)")
    print("3. Kitap Kirala")
    print("4. Kitap İade Et")
    
    # Hiyerarşik Yetki Kontrolü
    if ky.yetki_var_mi(kullanici, "personel"):
        print("5. Yeni Kitap Ekle")
        print("6. Stok Güncelle")
    
    if ky.yetki_var_mi(kullanici, "yonetici"):
        print("7. Kullanıcı Yönetimi (Admin Paneli)")
    
    print("0. Çıkış")
    return input("Seçiminiz: ")

def kitaplari_sirali_listele():
    kitaplar = kg.kitaplari_yukle()
    if not kitaplar:
        print("Kütüphanede kitap bulunamadı.")
        return
    
    print("\n--- Kitap Listesi (A-Z) ---")
    # Kitap ismine göre alfabetik sıralama
    sirali = sorted(kitaplar, key=lambda x: x.ad)
    for k in sirali:
        durum = "MEVCUT" if k.stok > 0 else "TÜKENDİ"
        print(f"[{k.isbn}] {k.ad} - {k.yazar} | Stok: {k.stok} | Durum: {durum}")

def kitap_kirala(kullanici):
    isbn = input("Kiralamak istediğiniz kitabın ISBN numarası: ")
    kitaplar = kg.kitaplari_yukle()
    
    for k in kitaplar:
        if k.isbn == isbn:
            if k.stok > 0:
                k.stok -= 1
                kg.kitaplari_kaydet(kitaplar)
                print(f"✓ {k.ad} başarıyla kiralandı. Kalan stok: {k.stok}")
                # Log tutma işlemi buraya eklenebilir
                return
            else:
                print("✗ Üzgünüz, bu kitabın stoğu tükenmiş.")
                return
    print("✗ Kitap bulunamadı.")

def kitap_iade(kullanici):
    isbn = input("İade etmek istediğiniz kitabın ISBN numarası: ")
    kitaplar = kg.kitaplari_yukle()
    
    for k in kitaplar:
        if k.isbn == isbn:
            k.stok += 1
            kg.kitaplari_kaydet(kitaplar)
            print(f"✓ {k.ad} iade alındı. Yeni stok: {k.stok}")
            return
    print("✗ Geçersiz ISBN.")

def ana_dongu():
    ky.sistem_hazirla()
    aktif_kullanici = ky.giris_yap()
    
    if not aktif_kullanici:
        return

    while True:
        secim = menuyu_goster(aktif_kullanici)
        
        if secim == "1":
            kitaplari_sirali_listele()
        elif secim == "3":
            kitap_kirala(aktif_kullanici)
        elif secim == "4":
            kitap_iade(aktif_kullanici)
        elif secim == "0":
            print("Güle güle!")
            break
        else:
            print("Bu özellik henüz geliştirme aşamasında veya yetkiniz yok.")

if __name__ == "__main__":
    ana_dongu()