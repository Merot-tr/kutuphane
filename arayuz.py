import tkinter as tk
from tkinter import messagebox, ttk
import kullanici_girisi_ve_yetkilendirme as kgy
import kitap_arama_listeleme as kal
import kitap_guncelleme as kg
import kullanici_hesap_yonetimi as khy
import Odunc_alma as oa
import raporlama as rp


class KutuphaneArayuz:
    def __init__(self, root):
        self.root = root
        self.root.title("Kütüphane Yönetim Sistemi")
        self.root.geometry("400x350")
        self.root.config(background="brown")
        self.aktif_kullanici = None
        
        # Pencere kapatıldığında arka planda terminalin asılı kalmaması için
        self.root.protocol("WM_DELETE_WINDOW", self.root.quit)
        
        # İkon yükleme (Hata vermemesi için try-except içine alındı)
        try:
            icon = tk.PhotoImage(file="book1.png")
            self.root.iconphoto(True, icon)
        except Exception:
            pass
            
        self.giris_ekrani_hazirla()

    def temizle(self):
        """Penceredeki tüm bileşenleri temizler (Ekranlar arası geçiş için)"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def giris_ekrani_hazirla(self):
        self.temizle()
        self.root.geometry("400x350")
        self.root.config(background="brown")
        
        tk.Label(self.root, text="KÜTÜPHANE SİSTEMİ GİRİŞİ", font=("Arial", 14, "bold"), bg="brown", fg="white").pack(pady=20)
        
        tk.Label(self.root, text="Kullanıcı Adı:", bg="brown", fg="white", font=("Arial", 10, "bold")).pack(pady=5)
        self.ent_kadi = tk.Entry(self.root, font=("Arial", 10))
        self.ent_kadi.pack()
        
        tk.Label(self.root, text="Şifre:", bg="brown", fg="white", font=("Arial", 10, "bold")).pack(pady=5)
        self.ent_sifre = tk.Entry(self.root, show="*", font=("Arial", 10))
        self.ent_sifre.pack()
        
        tk.Button(self.root, text="Giriş Yap", command=self.giris_kontrol, bg="green", fg="white", font=("Arial", 10, "bold"), width=15).pack(pady=25)

    def giris_kontrol(self):
        k_adi = self.ent_kadi.get().strip()
        sifre = self.ent_sifre.get().strip()
        
        if not k_adi or not sifre:
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun!")
            return
            
        kullanicilar = kgy.kullanicilari_yukle()
        for u in kullanicilar:
            if u.kullanici_adi == k_adi and kgy.sifre_dogru_mu(sifre, u.sifre_hash):
                self.aktif_kullanici = u
                # Diğer dosyaların 'u.adi' beklentisini bozmamak için yamalıyoruz
                self.aktif_kullanici.adi = u.kullanici_adi 
                messagebox.showinfo("Başarılı", f"Hoş geldiniz, {u.ad_soyad}!")
                self.ana_menu_hazirla()
                return
                
        messagebox.showerror("Hata", "Hatalı kullanıcı adı veya şifre!")

    def ana_menu_hazirla(self):
        self.temizle()
        self.root.geometry("500x550")
        self.root.config(background="brown")
        
        # Üst Bilgi Bandı
        bilgi_metni = f"Kullanıcı: {self.aktif_kullanici.ad_soyad} | Rol: {self.aktif_kullanici.rol.upper()}"
        tk.Label(self.root, text=bilgi_metni, bg="#3d2514", fg="white", font=("Arial", 10, "italic"), pady=5).pack(fill=tk.X)
        
        tk.Label(self.root, text="ANA MENÜ", font=("Arial", 16, "bold"), bg="brown", fg="white").pack(pady=15)
        
        # Standart Kullanıcı Butonları
        tk.Button(self.root, text="📚 Kitapları Listele", command=self.kitaplari_goster, width=30, height=2, font=("Arial", 10, "bold")).pack(pady=5)
        tk.Button(self.root, text="🔍 Kitap Ara", command=self.kitap_ara_penceresi, width=30, height=2, font=("Arial", 10, "bold")).pack(pady=5)
        tk.Button(self.root, text="🤝 Kitap Ödünç Al", command=self.kitap_odunc_penceresi, width=30, height=2, font=("Arial", 10, "bold")).pack(pady=5)
        tk.Button(self.root, text="↩ Kitap İade Et", command=self.kitap_iade_penceresi, width=30, height=2, font=("Arial", 10, "bold")).pack(pady=5)
        
        # Personel ve Üstü Yetkiler
        if kgy.yetki_var_mi(self.aktif_kullanici, "personel"):
            tk.Button(self.root, text="➕ [Personel] Yeni Kitap Ekle", command=self.kitap_ekle_penceresi, width=30, height=1, bg="#1a73e8", fg="white", font=("Arial", 10)).pack(pady=3)
            tk.Button(self.root, text="🔄 [Personel] Stok Güncelle", command=self.stok_guncelle_penceresi, width=30, height=1, bg="#1a73e8", fg="white", font=("Arial", 10)).pack(pady=3)
            tk.Button(self.root, text="📊 [Personel] Raporlama Paneli", command=self.raporlama_penceresi, width=30, height=1, bg="#1a73e8", fg="white", font=("Arial", 10)).pack(pady=3)
            
        # Sadece Yönetici Yetkisi
        if kgy.yetki_var_mi(self.aktif_kullanici, "yonetici"):
            tk.Button(self.root, text="👥 [Yönetici] Kullanıcı Yönetimi", command=self.kullanici_yonetimi_penceresi, width=30, height=1, bg="#d93025", fg="white", font=("Arial", 10, "bold")).pack(pady=5)
            
        tk.Button(self.root, text="🚪 Güvenli Çıkış", command=self.giris_ekrani_hazirla, width=30, bg="#3c4043", fg="white", font=("Arial", 10, "bold")).pack(pady=20)

    # 📚 KİTAP LİSTELEME
    def kitaplari_goster(self):
        yeni_pencere = tk.Toplevel(self.root)
        yeni_pencere.title("Kitap Listesi")
        yeni_pencere.geometry("700x400")
        
        kolonlar = ("isbn", "ad", "yazar", "stok", "konum")
        tablo = ttk.Treeview(yeni_pencere, columns=kolonlar, show="headings")
        
        tablo.heading("isbn", text="ISBN")
        tablo.heading("ad", text="Kitap Adı")
        tablo.heading("yazar", text="Yazar")
        tablo.heading("stok", text="Stok")
        tablo.heading("konum", text="Konum")
        
        tablo.column("isbn", width=120, anchor=tk.CENTER)
        tablo.column("ad", width=220)
        tablo.column("yazar", width=150)
        tablo.column("stok", width=60, anchor=tk.CENTER)
        tablo.column("konum", width=100, anchor=tk.CENTER)
        
        kitaplar = kg.kitaplari_yukle()
        kitaplar.sort(key=lambda k: k.ad.lower())
        for k in kitaplar:
            tablo.insert("", tk.END, values=(k.isbn, k.ad, k.yazar, k.stok, k.konum))
            
        tablo.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # 🔍 KİTAP ARAMA
    def kitap_ara_penceresi(self):
        yeni_pencere = tk.Toplevel(self.root)
        yeni_pencere.title("Kitap Ara")
        yeni_pencere.geometry("650x450")

        tk.Label(yeni_pencere, text="Aranacak Kelime:").pack(pady=5)
        ent_aranan = tk.Entry(yeni_pencere, width=30)
        ent_aranan.pack(pady=2)

        tk.Label(yeni_pencere, text="Arama Kriteri:").pack(pady=5)
        cmb_kriter = ttk.Combobox(yeni_pencere, values=["Ada Göre", "Yazara Göre", "ISBN'ye Göre"], state="readonly")
        cmb_kriter.current(0)
        cmb_kriter.pack(pady=2)

        kolonlar = ("isbn", "ad", "yazar", "stok", "konum")
        tablo = ttk.Treeview(yeni_pencere, columns=kolonlar, show="headings")
        for col in kolonlar:
            tablo.heading(col, text=col.upper())
            tablo.column(col, width=100)
        tablo.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        def ara():
            for i in tablo.get_children(): tablo.delete(i)
            kelime = ent_aranan.get().strip().lower()
            kriter = cmb_kriter.get()
            kitaplar = kg.kitaplari_yukle()
            
            if kriter == "Ada Göre":
                sonuclar = [k for k in kitaplar if kelime in k.ad.lower()]
            elif kriter == "Yazara Göre":
                sonuclar = [k for k in kitaplar if kelime in k.yazar.lower()]
            else:
                sonuclar = [k for k in kitaplar if kelime in k.isbn.lower()]

            for k in sonuclar:
                tablo.insert("", tk.END, values=(k.isbn, k.ad, k.yazar, k.stok, k.konum))
            if not sonuclar:
                messagebox.showinfo("Bilgi", "Eşleşen kitap bulunamadı.")

        tk.Button(yeni_pencere, text="Ara", command=ara, bg="blue", fg="white").pack(pady=5)

    # 🤝 ÖDÜNÇ ALMA
    def kitap_odunc_penceresi(self):
        yeni_pencere = tk.Toplevel(self.root)
        yeni_pencere.title("Kitap Ödünç Al")
        yeni_pencere.geometry("300x150")

        tk.Label(yeni_pencere, text="Ödünç Alınacak Kitap ISBN:").pack(pady=10)
        ent_isbn = tk.Entry(yeni_pencere)
        ent_isbn.pack()

        def islem_yap():
            isbn = ent_isbn.get().strip()
            if not isbn: return
            # Terminaldeki input mekanizmasını bypass etmek için doğrudan arka plan fonksiyonunu çağırıyoruz
            # Not: Odunc_alma.py içinde print yerine messagebox kullanacak şekilde revize edilebilir,
            # ya da burada doğrudan o kuralı taklit edebiliriz:
            try:
                kitaplar = kg.kitaplari_yukle()
                hedef_kitap = next((k for k in kitaplar if k.isbn == isbn), None)
                if not hedef_kitap:
                    messagebox.showerror("Hata", "Kitap bulunamadı!")
                    return
                if hedef_kitap.stok <= 0:
                    messagebox.showerror("Hata", "Bu kitabın stoğu tükenmiş!")
                    return
                
                # Odunc_alma modülünün işini elle tetikliyoruz (terminal inputunu süzmek adına)
                import datetime
                oduncler = oa.oduncleri_yukle()
                yeni_kayit = oa.OduncKaydi(
                    kayit_id=oa.kayit_id_olustur(),
                    isbn=isbn,
                    kullanici_adi=self.aktif_kullanici.kullanici_adi,
                    odunc_tarihi=str(datetime.date.today()),
                    iade_tarihi=str(datetime.date.today() + datetime.timedelta(days=14)),
                    geri_donus_tarihi=""
                )
                oduncler.append(yeni_kayit)
                oa.oduncleri_kaydet(oduncler)
                oa.kitap_stok_guncelle(isbn, -1)
                messagebox.showinfo("Başarılı", f"'{hedef_kitap.ad}' başarıyla ödünç alındı!\nSon İade: {yeni_kayit.iade_tarihi}")
                yeni_pencere.destroy()
            except Exception as e:
                messagebox.showerror("Hata", str(e))

        tk.Button(yeni_pencere, text="Ödünç Al", command=islem_yap, bg="green", fg="white").pack(pady=10)

    # ↩ İADE ETME
    def kitap_iade_penceresi(self):
        yeni_pencere = tk.Toplevel(self.root)
        yeni_pencere.title("Kitap İade Et")
        yeni_pencere.geometry("300x150")

        tk.Label(yeni_pencere, text="İade Edilecek Kitap ISBN:").pack(pady=10)
        ent_isbn = tk.Entry(yeni_pencere)
        ent_isbn.pack()

        def islem_yap():
            isbn = ent_isbn.get().strip()
            if not isbn: return
            try:
                oduncler = oa.oduncleri_yukle()
                kayit = next((o for o in oduncler if o.isbn == isbn and o.kullanici_adi == self.aktif_kullanici.kullanici_adi and not o.geri_donus_tarihi), None)
                if not kayit:
                    messagebox.showerror("Hata", "Üzerinizde bu ISBN'e ait aktif bir ödünç kaydı bulunamadı!")
                    return
                
                import datetime
                bugun = datetime.date.today()
                kayit.geri_donus_tarihi = str(bugun)
                oa.oduncleri_kaydet(oduncler)
                oa.kitap_stok_guncelle(isbn, +1)
                
                mesaj = "Kitap başarıyla iade alındı."
                iade_vakti = datetime.date.fromisoformat(kayit.iade_tarihi)
                if bugun > iade_vakti:
                    mesaj += f"\n⚠ { (bugun - iade_vakti).days } gün gecikmeli iade yaptınız!"
                    
                messagebox.showinfo("İade Başarılı", mesaj)
                yeni_pencere.destroy()
            except Exception as e:
                messagebox.showerror("Hata", str(e))

        tk.Button(yeni_pencere, text="İade Et", command=islem_yap, bg="green", fg="white").pack(pady=10)

    # ➕ YENİ KİTAP EKLEME
    def kitap_ekle_penceresi(self):
        yeni_pencere = tk.Toplevel(self.root)
        yeni_pencere.title("Yeni Kitap Ekle")
        yeni_pencere.geometry("300x350")

        alanlar = ["ISBN", "Kitap Adı", "Yazar", "Stok", "Konum (Raf)"]
        entries = {}
        for alan in alanlar:
            tk.Label(yeni_pencere, text=f"{alan}:").pack(pady=2)
            e = tk.Entry(yeni_pencere)
            e.pack(pady=2)
            entries[alan] = e

        def kaydet():
            isbn = entries["ISBN"].get().strip()
            ad = entries["Kitap Adı"].get().strip()
            yazar = entries["Yazar"].get().strip()
            stok = entries["Stok"].get().strip()
            konum = entries["Konum (Raf)"].get().strip()

            if not (isbn and ad and yazar and stok and konum):
                messagebox.showerror("Hata", "Lütfen tüm alanları doldurun!")
                return

            kitaplar = kg.kitaplari_yukle()
            if any(k.isbn == isbn for k in kitaplar):
                messagebox.showerror("Hata", "Bu ISBN numarası zaten kayıtlı!")
                return

            try:
                stok_sayi = int(stok)
                if stok_sayi < 0: raise ValueError
            except ValueError:
                messagebox.showerror("Hata", "Stok miktarı pozitif bir tam sayı olmalıdır!")
                return

            yeni_kitap = kg.Kitap(isbn, ad, yazar, stok_sayi, konum)
            kitaplar.append(yeni_kitap)
            kg.kitaplari_kaydet(kitaplar)
            messagebox.showinfo("Başarılı", f"'{ad}' kitabı sisteme eklendi.")
            yeni_pencere.destroy()

        tk.Button(yeni_pencere, text="Sisteme Kaydet", command=kaydet, bg="green", fg="white").pack(pady=15)

    # 🔄 STOK GÜNCELLEME
    def stok_guncelle_penceresi(self):
        yeni_pencere = tk.Toplevel(self.root)
        yeni_pencere.title("Stok Güncelle")
        yeni_pencere.geometry("300x180")

        tk.Label(yeni_pencere, text="Güncellenecek Kitap ISBN:").pack()
        ent_isbn = tk.Entry(yeni_pencere)
        ent_isbn.pack(pady=2)

        tk.Label(yeni_pencere, text="Yeni Stok Miktarı:").pack()
        ent_stok = tk.Entry(yeni_pencere)
        ent_stok.pack(pady=2)

        def guncelle():
            isbn = ent_isbn.get().strip()
            yeni_stok_str = ent_stok.get().strip()
            
            if not isbn or not yeni_stok_str:
                messagebox.showerror("Hata", "Lütfen tüm alanları doldurun.")
                return

            try:
                yeni_stok = int(yeni_stok_str)
                if yeni_stok < 0: raise ValueError
            except ValueError:
                messagebox.showerror("Hata", "Geçerli bir stok sayısı girin.")
                return

            kitaplar = kg.kitaplari_yukle()
            for k in kitaplar:
                if k.isbn == isbn:
                    k.stok = yeni_stok
                    kg.kitaplari_kaydet(kitaplar)
                    messagebox.showinfo("Başarılı", f"'{k.ad}' kitabının stoğu {yeni_stok} olarak güncellendi.")
                    yeni_pencere.destroy()
                    return
            messagebox.showerror("Hata", "Kitap bulunamadı.")

        tk.Button(yeni_pencere, text="Güncelle", command=guncelle, bg="blue", fg="white").pack(pady=10)

    # 👥 KULLANICI YÖNETİMİ
    def kullanici_yonetimi_penceresi(self):
        yeni_pencere = tk.Toplevel(self.root)
        yeni_pencere.title("Kullanıcı Yönetimi")
        yeni_pencere.geometry("600x450")

        tk.Label(yeni_pencere, text="Sistemdeki Kullanıcılar", font=("Arial", 12, "bold")).pack(pady=5)

        kolonlar = ("kadi", "adsoyad", "rol", "ogrno")
        tablo = ttk.Treeview(yeni_pencere, columns=kolonlar, show="headings", height=8)
        tablo.heading("kadi", text="Kullanıcı Adı")
        tablo.heading("adsoyad", text="Ad Soyad")
        tablo.heading("rol", text="Rol")
        tablo.heading("ogrno", text="Öğrenci No")
        tablo.pack(fill=tk.X, padx=10, pady=5)

        def listeyi_yenile():
            for i in tablo.get_children(): tablo.delete(i)
            for u in kgy.kullanicilari_yukle():
                tablo.insert("", tk.END, values=(u.kullanici_adi, u.ad_soyad, u.rol, u.ogrenci_no))

        listeyi_yenile()

        # Ekleme Bölümü
        lf = tk.LabelFrame(yeni_pencere, text="Yeni Kullanıcı Ekle")
        lf.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(lf, text="K.Adı:").grid(row=0, column=0, padx=2, pady=2)
        e_ka = tk.Entry(lf, width=12); e_ka.grid(row=0, column=1, padx=2, pady=2)

        tk.Label(lf, text="Şifre:").grid(row=0, column=2, padx=2, pady=2)
        e_sf = tk.Entry(lf, width=12, show="*"); e_sf.grid(row=0, column=3, padx=2, pady=2)

        tk.Label(lf, text="Ad Soyad:").grid(row=1, column=0, padx=2, pady=2)
        e_as = tk.Entry(lf, width=12); e_as.grid(row=1, column=1, padx=2, pady=2)

        tk.Label(lf, text="Öğr No:").grid(row=1, column=2, padx=2, pady=2)
        e_on = tk.Entry(lf, width=12); e_on.grid(row=1, column=3, padx=2, pady=2)

        tk.Label(lf, text="Rol:").grid(row=0, column=4, padx=2, pady=2)
        c_rl = ttk.Combobox(lf, values=["yonetici", "personel", "ogrenci"], width=10, state="readonly")
        c_rl.current(2); c_rl.grid(row=0, column=5, padx=2, pady=2)

        def k_ekle():
            ka, sf, as_ , on, rl = e_ka.get().strip(), e_sf.get().strip(), e_as.get().strip(), e_on.get().strip(), c_rl.get()
            if not (ka and sf and as_):
                messagebox.showerror("Hata", "Kullanıcı adı, şifre ve ad soyad zorunludur!")
                return
            kullanicilar = kgy.kullanicilari_yukle()
            if any(u.kullanici_adi == ka for u in kullanicilar):
                messagebox.showerror("Hata", "Bu kullanıcı adı zaten mevcut!")
                return
            
            yeni_u = kgy.Kullanici(ka, kgy.sifrele(sf), rl, as_, on if rl == "ogrenci" else "")
            kullanicilar.append(yeni_u)
            kgy.kullanicilari_kaydet(kullanicilar)
            messagebox.showinfo("Başarılı", "Kullanıcı oluşturuldu.")
            listeyi_yenile()

        tk.Button(lf, text="Ekle", command=k_ekle, bg="green", fg="white", width=10).grid(row=1, column=5, padx=5, pady=5)

        def k_sil():
            secili = tablo.selection()
            if not secili:
                messagebox.showwarning("Uyarı", "Lütfen silmek istediğiniz kullanıcıyı tablodan seçin.")
                return
            k_adi = tablo.item(secili[0])['values'][0]
            if k_adi == self.aktif_kullanici.kullanici_adi:
                messagebox.showerror("Hata", "Kendi hesabınızı silemezsiniz!")
                return
            
            if messagebox.askyesno("Onay", f"'{k_adi}' kullanıcısını silmek istediğinize emin misiniz?"):
                kullanicilar = kgy.kullanicilari_yukle()
                yeni_liste = [u for u in kullanicilar if u.kullanici_adi != k_adi]
                kgy.kullanicilari_kaydet(yeni_liste)
                messagebox.showinfo("Başarılı", "Kullanıcı silindi.")
                listeyi_yenile()

        tk.Button(yeni_pencere, text="Seçili Kullanıcıyı Sil", command=k_sil, bg="red", fg="white").pack(pady=5)

    # 📊 RAPORLAMA PANELI
    def raporlama_penceresi(self):
        yeni_pencere = tk.Toplevel(self.root)
        yeni_pencere.title("İstatistik ve Raporlama")
        yeni_pencere.geometry("500x400")

        txt_rapor = tk.Text(yeni_pencere, wrap=tk.WORD, font=("Courier", 10))
        txt_rapor.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        def rapor_getir(tip):
            txt_rapor.delete("1.0", tk.END)
            kitaplar = kg.kitaplari_yukle()
            oduncler = oa.oduncleri_yukle()
            import datetime
            
            if tip == "envanter":
                toplam_kitap = len(kitaplar)
                toplam_stok = sum(k.stok for k in kitaplar)
                txt_rapor.insert(tk.END, f"--- ENVANTER ÖZETİ ---\n\nToplam Benzersiz Kitap Sorumluluğu: {toplam_kitap}\nDepolardaki Toplam Kitap Adedi: {toplam_stok}\n")
            
            elif tip == "populer":
                from collections import Counter
                isbns = [o.isbn for o in oduncler]
                sayac = Counter(isbns).most_common(5)
                txt_rapor.insert(tk.END, "--- EN POPÜLER 5 KİTAP ---\n\n")
                for isbn, adet in sayac:
                    kitap = next((k for k in kitaplar if k.isbn == isbn), None)
                    ad = kitap.ad if kitap else "Bilinmeyen Kitap"
                    txt_rapor.insert(tk.END, f"-> {ad} (ISBN: {isbn}) - {adet} kez ödünç alındı.\n")
                    
            elif tip == "gecikme":
                bugun = datetime.date.today()
                txt_rapor.insert(tk.END, "--- GECİKMİŞ İADELER ---\n\n")
                say = 0
                for o in oduncler:
                    if o.geri_donus_tarihi: continue
                    if bugun > datetime.date.fromisoformat(o.iade_tarihi):
                        gecikme = (bugun - datetime.date.fromisoformat(o.iade_tarihi)).days
                        kitap = next((k for k in kitaplar if k.isbn == o.isbn), None)
                        ad = kitap.ad if kitap else o.isbn
                        txt_rapor.insert(tk.END, f"Kullanıcı: {o.kullanici_adi} | Kitap: {ad} | {gecikme} Gün Gecikmiş!\n")
                        say += 1
                if say == 0: txt_rapor.insert(tk.END, "Gecikmiş ödünç kaydı bulunmuyor.")

        bf = tk.Frame(yeni_pencere)
        bf.pack(pady=5)
        tk.Button(bf, text="Envanter", command=lambda: rapor_getir("envanter"), width=12).grid(row=0, column=0, padx=5)
        tk.Button(bf, text="Popülerler", command=lambda: rapor_getir("populer"), width=12).grid(row=0, column=1, padx=5)
        tk.Button(bf, text="Gecikenler", command=lambda: rapor_getir("gecikme"), width=12).grid(row=0, column=2, padx=5)

        rapor_getir("envanter") # Varsayılan olarak envanteri göster

if __name__ == "__main__":
    kgy.sistem_hazirla()
    root = tk.Tk()
    uygulama = KutuphaneArayuz(root)
    root.mainloop()