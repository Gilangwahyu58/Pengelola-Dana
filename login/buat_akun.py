from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from database import AdminLogin  # Pastikan ini diimpor
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel 


class BuatAkunScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.notification_label = None

    def on_enter(self):
        # Hapus label notifikasi jika ada
        if self.notification_label:
            self.remove_widget(self.notification_label)
        
        # Tambahkan label notifikasi baru
        self.notification_label = Label(text='', size_hint=(1, 0.1), color=(1, 0, 0, 1))
        self.add_widget(self.notification_label)

    def buat_akun(self):
        nama = self.ids.nama_lengkap.text
        username = self.ids.username.text
        no_telepon = self.ids.no_telepon.text
        kata_sandi = self.ids.kata_sandi.text

        if not all([nama, username, no_telepon, kata_sandi]):
            self.show_notification("Silahkan isi semua input yang sudah tersedia!")
            return

        # Memeriksa apakah nama pengguna sudah ada
        if not AdminLogin.is_nama_pengguna_unik(username):
            self.show_notification("Nama pengguna sudah terpakai! Silakan pilih yang lain.")
            return

        # Jika nama pengguna unik, simpan data dasar pengguna dan arahkan ke layar tautkan akun
        self.manager.current = 'tautkan_akun'
        # Menyimpan data sementara di session atau global jika diperlukan

    def show_notification(self, message):
        # Buat layout untuk dialog
        dialog_content = MDBoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Buat label untuk teks di tengah dialog
        label = MDLabel(
            text=message,  # Gunakan pesan yang diberikan
            theme_text_color='Custom',
            text_color=(1, 1, 1, 1),  # Warna teks putih
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
            size=(300, 20),  # Ukuran dialog yang lebih sesuai
            md_bg_color=[0, 0, 0, 1],  # Warna latar belakang dialog
            auto_dismiss=True,  
        )
        
        # Menampilkan dialog
        self.dialog.open()
        # Atur posisi dialog ke atas
        self.dialog.pos_hint = {'center_x': 0.5, 'top': 0.99}  # Posisi di tengah horizontal dan atas
        # Jadwalkan penutupan dialog setelah 1.5 detik
        Clock.schedule_once(self.close_dialog, 20)

    def close_dialog(self, *args):
        self.dialog.dismiss()  # Menutup dialog