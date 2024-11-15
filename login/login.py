from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from database import AdminLogin

class LoginScreen(Screen):
    def login(self):
        username = self.ids.username.text
        kata_sandi = self.ids.kata_sandi.text
        print(f"Login attempt with: {username}, {kata_sandi}")

        # Mengautentikasi pengguna
        user_data = AdminLogin.authenticate_user(username, kata_sandi)
        if user_data:
            # Simpan nama pengguna dan ID akun pengguna yang sedang login
            self.manager.current_screen.nama_pengguna = user_data.get('namaPengguna')  # Simpan nama pengguna
            self.manager.current_screen.akun_id = user_data.get('id')  # Simpan ID akun
            self.manager.current_screen.nama_desa = user_data.get('namaDesa')  # Set nama desa pengguna
            
            # Set username di pengaturan akun
            self.manager.get_screen('user_pengaturan_akun').current_username = user_data.get('namaPengguna')  # Set the current username
            
            # Ambil nama lengkap dari user_data
            nama_lengkap = user_data.get('namaLengkap', 'User  ')  # Default ke 'User  ' jika tidak ada
            nama_desa = user_data.get('namaDesa', 'Desa Tidak Diketahui')  # Ambil nama desa

            # Simpan nama desa di PenggunaanTambahScreen
            penggunaan_tambah_screen = self.manager.get_screen('penggunaan_tambah')
            penggunaan_tambah_screen.nama_desa = nama_desa

            if user_data.get('role') == 'admin':
                self.show_popup(f"Selamat datang Admin, {nama_lengkap}")
                self.manager.current = 'adm_beranda'
            else:
                self.show_popup(f"Selamat datang, {nama_lengkap}")
                self.manager.current = 'peng_beranda'

            # Mengosongkan input setelah login berhasil
            self.ids.username.text = ""  # Mengosongkan input username
            self.ids.kata_sandi.text = ""  # Mengosongkan input kata sandi
        else:
            self.show_popup("Periksa nama pengguna dan kata sandi.")    
            
    def show_popup(self, message):
        # Buat layout untuk dialog
        dialog_content = MDBoxLayout(orientation='vertical', padding=10, spacing=10)

        # Buat label untuk pesan dialog
        message_label = MDLabel(
            text=message,
            theme_text_color='Custom',
            text_color=(1, 1, 1, 1),  
            font_style='Body2',  # Menggunakan gaya font yang lebih kecil untuk pesan
            halign='center',
            size_hint_y=None,
            height=20  # Tinggi label pesan
        )
        dialog_content.add_widget(message_label)

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