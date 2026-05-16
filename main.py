import os
import sys
import kitap_guncelleme as kg
import kullanici_girisi_ve_yetkilendirme as kgy
import kullanici_hesap_yonetimi as khy
import kitap_arama_listeleme as kal
import Odunc_alma as oa
import raporlama as rp

def menuyu_goster(kullanici):
    print(f"\n--- {kullanici.ad_soyad.upper()} ({kullanici.rol}) ---")
    print("1. Kitapları Listele (Sıralı)")
    print("2. Kitap Ara (İsim/ISBN)")
    print("3. Kitap Ödünç Al")
    print("4. Kitap İade Et")
    
    # Personel ve Üstü Yetkiler
    if kgy.yetki_var_mi(kullanici, "personel"):
        print("5. Yeni Kitap Ekle")
        print("6. Stok Güncelle")
        print("7. İstatistik ve Raporlama Paneli")
    
    # Sadece Yönetici Yetkisi
    if kgy.yetki_var_mi(kullanici, "yonetici"):
        print("8. Kullanıcı Yönetim Paneli")
    
    print("0. Çıkış")
    return input("Seçiminiz: ").strip()

def alt_menü_kullanici_yonetimi(aktif_kullanici):
    while True:
        print("\n--- Kullanıcı Yönetim Paneli ---")
        print("1. Kullanıcı Oluştur")
        print("2. Kullanıcı Sil")
        print("3. Kullanıcıları Listele")
        print("0. Ana Menüye Dön")
        secim = input("Seçiminiz: ").strip()

        if secim == "1":
            khy.kullanici_olustur()
        elif secim == "2":
            khy.kullanici_sil(aktif_kullanici)
        elif secim == "3":
            khy.kullanicilari_listele()
        elif secim == "0":
            break
        else:
            print("Geçersiz seçim.")

def alt_menü_raporlama():
    while True:
        print("\n--- İstatistik ve Raporlama Paneli ---")
        print("1. Envanter Özeti")
        print("2. Popüler Kitaplar")
        print("3. Gecikmiş İadeler")
        print("4. Tam Rapor Çıkar")
        print("0. Ana Menüye Dön")
        secim = input("Seçiminiz: ").strip()

        if secim == "1":
            rp.envanter_ozeti()
        elif secim == "2":
            rp.populer_kitaplar()
        elif secim == "3":
            rp.gecikmis_iadeler()
        elif secim == "4":
            rp.tam_rapor()
        elif secim == "0":
            break
        else:
            print("Geçersiz seçim.")

def ana_dongu():
    kgy.sistem_hazirla()
    aktif_kullanici = kgy.giris_yap()
    
    if not aktif_kullanici:
        return

    # Odunc_alma.py dosyasındaki '.adi' hatasını dinamik olarak düzeltiyoruz
    # Böylece harici dosyayı değiştirmek zorunda kalmazsınız.
    aktif_kullanici.adi = aktif_kullanici.kullanici_adi

    while True:
        secim = menuyu_goster(aktif_kullanici)
        
        if secim == "1":
            kal.kitaplari_listele()
        elif secim == "2":
            kal.kitap_ara()
        elif secim == "3":
            oa.odunc_al(aktif_kullanici)
        elif secim == "4":
            oa.iade_et(aktif_kullanici)
        elif secim == "5" and kgy.yetki_var_mi(aktif_kullanici, "personel"):
            kg.kitap_ekle()
        elif secim == "6" and kgy.yetki_var_mi(aktif_kullanici, "personel"):
            kg.stok_guncelle()
        elif secim == "7" and kgy.yetki_var_mi(aktif_kullanici, "personel"):
            alt_menü_raporlama()
        elif secim == "8" and kgy.yetki_var_mi(aktif_kullanici, "yonetici"):
            alt_menü_kullanici_yonetimi(aktif_kullanici)
        elif secim == "0":
            print("Güle güle!")
            break
        else:
            print("Bu özellik henüz geliştirme aşamasında veya yetkiniz yok.")

if __name__ == "__main__":
    ana_dongu()