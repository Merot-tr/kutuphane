import tkinter as tk
from tkinter import messagebox, ttk
import kullanici_girisi_ve_yetkilendirme as kgy
import kitap_arama_listeleme as kal
import kitap_guncelleme as kg

class KutuphaneArayuz:
    def __init__(self, root):
        self.root = root
        self.root.title("Kütüphane Yönetim Sistemi")
        self.root.geometry("400x300")
        icon = tk.PhotoImage(file="book1.png")  # Simge dosyasının yolunu belirtin
        self.root.iconphoto(True, icon)
        self.root.config(background="brown")
        self.aktif_kullanici = None
        
        # İlk olarak giriş ekranını yükle
        self.giris_ekrani_hazirla()

    def temizle(self):
        """Penceredeki tüm bileşenleri temizler (Ekranlar arası geçiş için)"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def giris_ekrani_hazirla(self):
        self.temizle()
        self.root.geometry("400x300")
        
        tk.Label(self.root, text="KÜTÜPHANE SİSTEMİ GİRİŞİ", font=("Arial", 14, "bold")).pack(pady=20)
        
        tk.Label(self.root, text="Kullanıcı Adı:").pack(pady=5)
        self.ent_kadi = tk.Entry(self.root)
        self.ent_kadi.pack()
        
        tk.Label(self.root, text="Şifre:").pack(pady=5)
        self.ent_sifre = tk.Entry(self.root, show="*")
        self.ent_sifre.pack()
        
        tk.Button(self.root, text="Giriş Yap", command=self.giris_kontrol, bg="green", fg="white").pack(pady=20)

    def giris_kontrol(self):
        k_adi = self.ent_kadi.get().strip()
        sifre = self.ent_sifre.get().strip()
        
        # Mevcut giriş fonksiyonunu kullanıyoruz
        kullanicilar = kgy.kullanicilari_yukle()
        for u in kullanicilar:
            if u.kullanici_adi == k_adi and kgy.sifre_dogru_mu(sifre, u.sifre_hash):
                self.aktif_kullanici = u
                messagebox.showinfo("Başarılı", f"Hoş geldiniz, {u.ad_soyad}!")
                self.ana_menu_hazirla()
                return
                
        messagebox.showerror("Hata", "Hatalı kullanıcı adı veya şifre!")

    def ana_menu_hazirla(self):
        self.temizle()
        self.root.geometry("600x400")
        
        # Üst Bilgi Bandı
        bilgi_metni = f"Kullanıcı: {self.aktif_kullanici.ad_soyad} | Rol: {self.aktif_kullanici.rol.upper()}"
        tk.Label(self.root, text=bilgi_metni, bg="gray", fg="white").pack(fill=tk.X)
        
        tk.Label(self.root, text="ANA MENÜ", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Herkesin Görebileceği Butonlar
        tk.Button(self.root, text="Kitapları Listele", command=self.kitaplari_goster, width=25).pack(pady=5)
        
        # Yetki Kontrollerine Göre Buton Ekleme
        if kgy.yetki_var_mi(self.aktif_kullanici, "personel"):
            tk.Button(self.root, text="[Personel] Yeni Kitap Ekle", command=self.kitap_ekle_penceresi, width=25, fg="blue").pack(pady=5)
            tk.Button(self.root, text="[Personel] Stok Güncelle", width=25, fg="blue").pack(pady=5)
            
        if kgy.yetki_var_mi(self.aktif_kullanici, "yonetici"):
            tk.Button(self.root, text="[Yönetici] Kullanıcı Yönetimi", width=25, fg="red").pack(pady=5)
            
        tk.Button(self.root, text="Çıkış", command=self.giris_ekrani_hazirla, width=25, bg="darkred", fg="white").pack(pady=20)

    def kitaplari_goster(self):
        """Kitapları bir tablo (Treeview) içinde yeni bir pencerede gösterir"""
        yeni_pencere = tk.Toplevel(self.root)
        yeni_pencere.title("Kitap Listesi")
        yeni_pencere.geometry("700x400")
        
        # Tablo Yapısı (Treeview)
        kolonlar = ("isbn", "ad", "yazar", "stok", "konum")
        tablo = ttk.Treeview(yeni_pencere, columns=kolonlar, show="headings")
        
        # Başlıkları Tanımla
        tablo.heading("isbn", text="ISBN")
        tablo.heading("ad", text="Kitap Adı")
        tablo.heading("yazar", text="Yazar")
        tablo.heading("stok", text="Stok")
        tablo.heading("konum", text="Konum")
        
        # Genişlikleri Ayarla
        tablo.column("isbn", width=100)
        tablo.column("ad", width=200)
        tablo.column("yazar", width=150)
        tablo.column("stok", width=50)
        tablo.column("konum", width=100)
        
        # Verileri Yükle (Mevcut kodundaki fonksiyonu çağırıyoruz)
        kitaplar = kg.kitaplari_yukle()
        for k in kitaplar:
            tablo.insert("", tk.END, values=(k.isbn, k.ad, k.yazar, k.stok, k.konum))
            
        tablo.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def kitap_ekle_penceresi(self):
        """Yeni kitap eklemek için form penceresi açar"""
        # Bu kısmı da yukarıdaki mantıkla Entry'ler koyup butonun 'command' kısmına 
        # kg.kitap_ekle() fonksiyonundaki mantığı tkinter entegreli yazarak geliştirebilirsin.
        pass

if __name__ == "__main__":
    kgy.sistem_hazirla() # İlk admin kontrolü
    root = tk.Tk()
    uygulama = KutuphaneArayuz(root)
    root.mainloop()