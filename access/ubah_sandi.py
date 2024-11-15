from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.clock import Clock
from database import AdminLogin  # Pastikan Anda sudah mengimpor AdminLogin dari database

class UbahSandiScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_enter(self):
        """Method ini dipanggil ketika layar ini ditampilkan."""
        try:
            nama_pengguna = self.manager.get_screen('login').nama_pengguna
            user_data = AdminLogin.db.child("login").order_by_child("namaPengguna").equal_to(nama_pengguna).get()

            if user_data.each():
                for user in user_data.each():
                    self.ids.kata_sandi_lama.text = ""  # Kosongkan input untuk kata sandi lama
                    self.kata_sandi_db = user.val().get("kataSandi", "")  # Ambil kata sandi dari database
            else:
                print("Data pengguna tidak ditemukan.")
        except Exception as e:
            print(f"Error saat memuat data pengguna: {e}")
    def on_leave(self):
        """Method ini dipanggil ketika layar ini ditutup."""
        self.ids.kata_sandi_lama.text = ""  # Kosongkan input kata sandi lama
        self.ids.kata_sandi_baru.text = ""   # Kosongkan input kata sandi baru
        self.ids.konfirmasi_kata_sandi.text = ""  # Kosongkan input konfirmasi kata sandi
    def ubah_sandi(self):
        """Method untuk mengubah kata sandi."""
        kata_sandi_lama = self.ids.kata_sandi_lama.text
        kata_sandi_baru = self.ids.kata_sandi_baru.text
        konfirmasi_kata_sandi = self.ids.konfirmasi_kata_sandi.text

        # Validasi kata sandi lama
        if kata_sandi_lama != self.kata_sandi_db:
            self.show_popup("Kata Sandi Salah", "Kata sandi lama yang Anda masukkan salah.")
            return

        # Validasi kata sandi baru dan konfirmasi
        if kata_sandi_baru != konfirmasi_kata_sandi:
            self.show_popup("Kata Sandi Tidak Sama", "Kata sandi baru dan konfirmasi kata sandi tidak sama.")
            return

        # Jika validasi berhasil, simpan kata sandi baru ke database
        try:
            nama_pengguna = self.manager.get_screen('login').nama_pengguna
            user_data = AdminLogin.db.child("login").order_by_child("namaPengguna").equal_to(nama_pengguna).get()
            if user_data.each():
                for user in user_data.each():
                    AdminLogin.db.child("login").child(user.key()).update({
                        "kataSandi": kata_sandi_baru  # Update kata sandi baru ke database
                    })
                self.show_popup("Sandi Berhasil Diubah", "Kata sandi Anda telah berhasil diperbarui.")
                 # Redirect to adm_profil screen
                self.manager.current = 'adm_profil'
            else:
                print("Data pengguna tidak ditemukan.")
        except Exception as e:
            print(f"Error saat memperbarui kata sandi: {e}")

    def show_popup(self, title, message):
         # Buat layout untuk dialog
        dialog_content = MDBoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Buat label untuk teks di tengah dialog
        label = MDLabel(
            text=message,
            theme_text_color='Custom',
            text_color=(1, 1, 1, 1),  # Warna teks 
            font_style='Body2',
            halign='center',
            size_hint_y=None,
            height=20  # Atur tinggi label agar sesuai
        )
        dialog_content.add_widget(label)

        # Buat dialog menggunakan KivyMD
        self.dialog = MDDialog(
            type='custom',
            content_cls=dialog_content,
            size_hint=(None, None),
            size=(265, 20),
            md_bg_color=[0, 0, 0, 1],  # Warna latar belakang dialog
            auto_dismiss=True, 
        )
        
        # Menampilkan dialog
        self.dialog.open()
         # Atur posisi dialog ke atas
        self.dialog.pos_hint = {'center_x': 0.5, 'top': 0.99}  # Posisi di tengah horizontal dan atas


        # Jadwalkan penutupan dialog setelah 1 detik
        Clock.schedule_once(self.close_dialog, 10)

    def close_dialog(self, *args):
        self.dialog.dismiss()  # Menutup dialog