from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel 
from database import AdminLogin

class TautkanAkunScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.notification_label = None
        self.desa_list = []  # Menyimpan daftar desa

    def on_enter(self):
        # Hapus label notifikasi jika ada
        if self.notification_label:
            self.remove_widget(self.notification_label)
        
        # Tambahkan label notifikasi baru
        self.notification_label = Label(text='', size_hint=(1, 0.1), color=(1, 0, 0, 1))
        self.add_widget(self.notification_label)
        self.load_desa()  # Memanggil fungsi untuk memuat desa saat memasuki layar

    def load_desa(self):
        try:
            # Mengambil data desa dari database
            desa_data = AdminLogin.db.child("login").order_by_child("role").equal_to("admin").get()
            self.desa_list = [user.val().get('namaDesa') for user in desa_data.each() if isinstance(user.val(), dict)]
            self.ids.desa_spinner.values = self.desa_list  # Mengisi spinner dengan daftar desa
        except Exception as e:
            print(f"Error loading desa: {e}")
            self.show_notification("Gagal memuat daftar desa.")

    def kirim(self):
        nik = self.ids.nik.text
        no_kk = self.ids.no_kk.text
        nama_desa = self.ids.desa_spinner.text  # Ambil dari spinner nama desa

        if not all([nik, no_kk, nama_desa]):
            self.show_notification("Silahkan isi semua input yang sudah tersedia!")
            return
        
        # Mengambil nama pengguna otomatis
        base_username = self.manager.get_screen('buat_akun').ids.username.text
        namaPengguna = self.generate_namapengguna(base_username)

        # Menyimpan data pengguna ke database
        user_data = {
            'namaLengkap': self.manager.get_screen('buat_akun').ids.nama_lengkap.text,
            'username': self.manager.get_screen('buat_akun').ids.username.text,
            'namaPengguna': namaPengguna,
            'noTelepon': self.manager.get_screen('buat_akun').ids.no_telepon.text,
            'kataSandi': self.manager.get_screen('buat_akun').ids.kata_sandi.text,
            'nik': nik,
            'noKK': no_kk,
            'namaDesa': nama_desa,
            'role': 'pengguna'
        }

        try:
            # Push data ke database
            AdminLogin.db.child("login").push(user_data)
            self.show_notification("Akun berhasil dibuat!")
        except Exception as e:
            print(f"Error saving user data: {e}")
            self.show_notification("Terjadi kesalahan saat menyimpan akun. Silakan coba lagi.")

        # Reset input fields
        self.ids.nik.text = ""
        self.ids.no_kk.text = ""
        self.ids.desa_spinner.text = ""  # Reset spinner ke nilai kosong
        
        self.manager.current = 'login'  # Arahkan ke halaman login
    def generate_namapengguna(self, base_username):
        """Generate username baru berdasarkan input pengguna dan yang sudah ada di database."""
        try:
            # Mengambil semua pengguna dari database
            users_data = AdminLogin.db.child("login").get()
            existing_usernames = [user.val().get('username') for user in users_data.each() if isinstance(user.val(), dict)]

            # Jika nama pengguna tidak ada, gunakan nama pengguna input
            if base_username not in existing_usernames:
                return base_username
            
            # Jika nama pengguna sudah ada, tambahkan nomor urut
            counter = 1
            new_username = f"{base_username}{counter}"
            while new_username in existing_usernames:
                counter += 1
                new_username = f"{base_username}{counter}"
            
            return new_username
        except Exception as e:
            print(f"Error generating username: {e}")
            return base_username  # Kembali ke username dasar jika terjadi kesalahan
            
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