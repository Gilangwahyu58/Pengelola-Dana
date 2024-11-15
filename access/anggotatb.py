from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock  # Tambahkan import untuk Clock
from kivymd.uix.dialog import MDDialog  # Import MDDialog dari KivyMD
from kivymd.uix.label import MDLabel  # Import MDLabel dari KivyMD
from kivymd.uix.boxlayout import MDBoxLayout  # Import MDBoxLayout dari KivyMD
from database import Anggota
from kivy.app import App

class TambahAnggotaScreen(Screen):
    def on_enter(self):
        app = App.get_running_app()
        self.nama_desa = app.root.get_screen('adm_beranda').nama_desa  # Ambil nama desa dari layar beranda

    def add_anggota(self):
        # Ambil data dari input
        nama = self.ids.nama_input.text
        jabatan = self.ids.jabatan_input.text
        masa_periode = self.ids.masa_periode_input.text
        no_telp = self.ids.no_telp_input.text

        anggota_data = {
            'nama': nama,
            'jabatan': jabatan,
            'masaPeriode': masa_periode,
            'noTelp': no_telp,
            'namaDesa': self.nama_desa  # Menambahkan nama desa ke data anggota
        }

        # Menambahkan anggota ke database
        try:
            Anggota.add_anggota(anggota_data)
            self.show_popup("Anggota berhasil ditambahkan!")  # Tampilkan popup sukses
            self.clear_inputs()  # Mengosongkan input setelah menambahkan
        except Exception as e:
            print(f"Error adding member: {e}")
            self.show_popup("Gagal menambahkan anggota. Silakan coba lagi.")  # Tampilkan popup error

    def show_popup(self, message):
        dialog_content = MDBoxLayout(orientation='vertical', padding=10, spacing=10)
        
        label = MDLabel(
            text=message,
            theme_text_color='Custom',
            text_color=(1, 1, 1, 1),  # Warna teks 
            font_style='Body2',
            halign='center',
            size_hint_y=None,
            height=20
        )
        dialog_content.add_widget(label)

        self.dialog = MDDialog(
            type='custom',
            content_cls=dialog_content,
            size_hint=(None, None),
            size=(265, 100),
            md_bg_color=[0, 0, 0, 1],
            auto_dismiss=True, 
        )
        
        self.dialog.open()
        self.dialog.pos_hint = {'center_x':  0.5, 'top': 0.99}

        Clock.schedule_once(self.close_dialog, 10)

    def close_dialog(self, dt):
        """Menutup dialog."""
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None

    def clear_inputs(self):
        self.ids.nama_input.text = ''
        self.ids.jabatan_input.text = ''
        self.ids.masa_periode_input.text = ''
        self.ids.no_telp_input.text = ''