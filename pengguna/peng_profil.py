from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton
from database import AdminLogin  # Pastikan ini diimpor
from kivy.clock import Clock 

class PengProfileScreen(Screen):
    def __init__(self, **kwargs):
        super(PengProfileScreen, self).__init__(**kwargs)
        self.nama_pengguna = "Default User"  # ID akun saat ini
        self.dialog = None  # Untuk menyimpan instance dialog

    def on_enter(self):  # Method ini akan dipanggil saat layar ini ditampilkan
        """Method ini dipanggil ketika layar ini ditampilkan."""
        try:
            # Ambil nama pengguna dari layar login
            self.nama_pengguna = self.manager.get_screen('login').nama_pengguna
            
            # Ambil data pengguna dari AdminLogin
            user_data = AdminLogin.db.child("login").order_by_child("namaPengguna").equal_to(self.nama_pengguna).get()

            if user_data.each():
                for user in user_data.each():
                    self.ids.nama.text = user.val().get('username', 'Nama tidak ditemukan')
                    self.ids.foto_profil.source = user.val().get('fotoProfil', 'assets/image/orang.png')  # Ganti dengan foto profil default jika tidak ada
            else:
                self.ids.nama.text = 'Data tidak ditemukan'
                self.ids.foto_profil.source = 'assets/image/orang.png'  # Set foto profil default jika tidak ada data

        except Exception as e:
            print(f"Error: {e}")
            self.ids.nama.text = 'Error dalam mengambil data'
            self.ids.foto_profil.source = 'assets/image/orang.png'  # Set foto profil default jika terjadi error

    def update_profile_picture(self, new_picture_path):
        """Method untuk memperbarui foto profil."""
        try:
            # Ambil nama pengguna yang sedang login
            nama_pengguna = self.manager.get_screen('login').nama_pengguna
            
            # Update foto profil di database
            user_data = AdminLogin.db.child("login").order_by_child("namaPengguna").equal_to(nama_pengguna).get()
            
            if user_data.each():
                for user in user_data.each():
                    AdminLogin.db.child("login").child(user.key()).update({"fotoProfil": new_picture_path})
                    self.ids.foto_profil.source = new_picture_path  # Update foto profil di UI
            else:
                print("Pengguna tidak ditemukan saat memperbarui foto profil.")
        
        except Exception as e:
            print(f"Error saat memperbarui foto profil: {e}")
            
    def hapus_akun(self):
        # Tampilkan dialog konfirmasi
        self.dialog = MDDialog(
            title="Konfirmasi Hapus Akun",
            text="Apakah Anda yakin?",
            buttons=[
                MDFlatButton(
                    text="Tidak",
                    on_release=self.dismiss_dialog
                ),
                MDFlatButton(
                    text="Ya",
                    on_release=self.confirm_hapus_akun
                ),
            ],
        )
        self.dialog.open()

    def dismiss_dialog(self, *args):
        self.dialog.dismiss()  # Menutup dialog

    def confirm_hapus_akun(self, *args):
        self.dialog.dismiss()  # Menutup dialog
        self.akun_berhasil_dihapus()  # Memanggil fungsi untuk menghapus akun

    def akun_berhasil_dihapus(self):
        # Menghapus akun dari database
        success = AdminLogin.delete_akun(self.nama_pengguna)
        if success:
            # Buat layout untuk dialog
            dialog_content = MDBoxLayout(orientation='vertical', padding=10, spacing=10)

            # Buat label untuk teks di tengah dialog
            label = MDLabel(
                text='Akun berhasil dihapus.',
                theme_text_color='Custom',
                text_color=(1, 1, 1, 1),  # Warna teks hijau
                font_style='Body1',
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
                size=(265, 100),  # Ukuran dialog
                md_bg_color=[0, 0, 0, 1],  # Warna latar belakang dialog
                auto_dismiss=True,  # Agar tidak otomatis tertutup
            )
            
            # Menampilkan dialog
            self.dialog.open()
            # Atur posisi dialog ke atas
            self.dialog.pos_hint = {'center_x': 0.5, 'top': 0.99}  # Posisi di tengah horizontal dan atas

            # Jadwalkan penutupan dialog 
            Clock.schedule_once(self.navigate_to_beranda, 2.5)

        else:
            # Tampilkan dialog jika terjadi kesalahan saat menghapus
            dialog = MDDialog(
                title="Error",
                text="Terjadi kesalahan saat menghapus akun.",
                buttons=[
                    MDFlatButton(
                        text="OK",
                        on_release=self.dismiss_dialog
                    ),
                ],
            )
            dialog.open()

    def navigate_to_beranda(self, *args):
        self.dialog.dismiss()  # Menutup dialog sebelum navigasi
        self.manager.current = 'beranda'  # Ganti ke layar 'beranda'

    def build(self):
        layout = MDBoxLayout(orientation='vertical')
        # Tambahkan tombol hapus akun
        hapus_button = MDFlatButton(text="Hapus Akun")
        hapus_button.bind(on_press=self.hapus_akun)
        layout.add_widget(hapus_button)
        return layout

