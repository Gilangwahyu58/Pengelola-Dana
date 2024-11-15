from kivy.app import App
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from database import AdminLogin
from storage import StorageManager

class ImageSelectPopup(Popup):
    def __init__(self, on_select, **kwargs):
        super().__init__(**kwargs)
        self.title = 'Pilih Gambar'
        self.size_hint = (0.9, 0.9)
        self.on_select = on_select

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.file_chooser = FileChooserIconView(
            filters=['*.png', '*.jpg', '*.jpeg'],
            path='.'
        )
        layout.add_widget(self.file_chooser)

        button_layout = BoxLayout(size_hint_y=None, height=40, spacing=10)
        
        cancel_btn = Button(text='Batal')
        cancel_btn.bind(on_press=self.dismiss)
        
        select_btn = Button(text='Pilih', background_color=(0.3, 0.5, 0.9, 1))
        select_btn.bind(on_press=self.select_image)
        
        button_layout.add_widget(cancel_btn)
        button_layout.add_widget(select_btn)
        
        layout.add_widget(button_layout)
        self.content = layout

    def select_image(self, instance):
        if self.file_chooser.selection:
            self.on_select(self.file_chooser.selection[0])
            self.dismiss()

class UserPengaturanAkunScreen(Screen):
    def on_enter(self):
        """Method ini dipanggil ketika layar ini ditampilkan."""
        try:
            nama_pengguna = self.manager.get_screen('login').nama_pengguna
            user_data = AdminLogin.db.child("login").order_by_child("namaPengguna").equal_to(nama_pengguna).get()

            if user_data.each():
                for user in user_data.each():
                    print(user.val())  # Debug: tampilkan data pengguna
                    self.ids.username.text = user.val().get("username", "")
                    self.ids.nama_lengkap.text = user.val().get("namaLengkap", "")
                    self.ids.no_telepon.text = user.val().get("noTelepon", "")
                    foto_profil = user.val().get("fotoProfil", "assets/image/orang.png")
                    self.ids.image_preview.source = foto_profil  # Menggunakan ID yang benar
                    self.ids.image_preview.reload()  # Reload gambar untuk memastikan tampilan terbaru
                    print(f"Foto Profil: {foto_profil}")  # Debug: tampilkan sumber foto profil
                self.user_key = user.key()  # Simpan kunci pengguna untuk digunakan saat memperbarui data
            else:
                print("Data pengguna tidak ditemukan.")
        except Exception as e:
            print(f"Error saat memuat data pengguna: {e}")

    def open_image_selector(self):
        """Membuka popup untuk memilih gambar."""
        popup = ImageSelectPopup(on_select=self.update_image)
        popup.open()

    def update_image(self, image_path):
        """Mengupdate sumber gambar."""
        print(f"Updating image with path: {image_path}")  # Debugging
        self.ids.image_preview.source = image_path  # Update UI dengan gambar baru
        self.ids.image_preview.reload()  # Reload the image to show the new one
        print("Image source updated in UI.")  # Konfirmasi pembaruan UI

        # Panggil fungsi untuk mengunggah gambar menggunakan StorageManager
        upload_result = StorageManager.upload_profile_image(image_path)  # Menggunakan metode upload_profile_image
        if upload_result['status'] == "success":
            print(f"Image uploaded successfully: {upload_result['url']}")
            self.save_image_path(upload_result['url'])  # Simpan URL jika berhasil
        else:
            print("Failed to upload image.")

    def save_image_path(self, image_path):
        """Method untuk menyimpan path gambar ke database."""
        try:
            # Memperbarui data pengguna di database
            success = AdminLogin.db.child("login").child(self.user_key).update({
                "fotoProfil": image_path  # Simpan URL gambar di database
            })
            if success:
                print("Image path saved to database.")
            else:
                print("Failed to save image path to database.")
        except Exception as e:
            print(f"Error saving image path: {e}")

    def clear_image(self):
        """Menghapus gambar profil."""
        self.ids.image_preview.source = "assets/image/orang.png"  # Gambar default
        self.ids.image_preview.reload()  # Reload untuk memastikan tampilan terbaru
        print("Gambar profil dihapus.")

    def save_changes(self):
        """Method untuk menyimpan perubahan."""
        try:
            # Ambil ID pengguna dari layar login
            nama_pengguna = self.manager.get_screen('login').nama_pengguna
            
            # Ambil data dari input
            username = self.ids.username.text
            nama_lengkap = self.ids.nama_lengkap.text
            no_telepon = self.ids.no_telepon.text
            foto_profil = self.ids.image_preview.source  # Ambil path gambar saat ini
            
            # Memperbarui data pengguna di database
            success = AdminLogin.db.child("login").child(self.user_key).update({
                "username": username,
                "namaLengkap": nama_lengkap,
                "noTelepon": no_telepon,
                "fotoProfil": foto_profil
            })
            if success:
                print("Perubahan berhasil disimpan.")
                # Pindah ke layar 
                self.manager.current = 'peng_profil'
                # Tampilkan dialog sukses
                self.show_success_dialog()
            else:
                print("Gagal menyimpan perubahan.")
        except Exception as e:
            print(f"Error saat menyimpan perubahan: {e}")

    def show_success_dialog(self):
        # Buat layout untuk dialog
        dialog_content = MDBoxLayout(orientation='vertical', padding=10, spacing=10)

        # Buat label untuk teks di tengah dialog
        label = MDLabel(
            text='Perubahan berhasil disimpan',
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