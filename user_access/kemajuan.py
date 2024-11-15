from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel 

class KemajuanScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_kegiatan_click(self):
        self.show_login_popup()

    def show_login_popup(self):
        # Buat layout untuk dialog
        dialog_content = MDBoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Buat label untuk teks di tengah dialog
        label = MDLabel(
            text='Silahkan Login Terlebih Dahulu!',
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
            auto_dismiss=False,  # Agar tidak otomatis tertutup
        )
        
        # Menampilkan dialog
        self.dialog.open()
         # Atur posisi dialog ke atas
        self.dialog.pos_hint = {'center_x': 0.5, 'top': 0.99}  # Posisi di tengah horizontal dan atas


        # Jadwalkan penutupan dialog setelah 1 detik
        Clock.schedule_once(self.close_dialog, 1.2)

    def close_dialog(self, *args):
        self.dialog.dismiss()  # Menutup dialog
