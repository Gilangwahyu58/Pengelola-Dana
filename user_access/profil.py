from kivy.uix.screenmanager import Screen
import webbrowser
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
import platform

class ProfileScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_login_click(self):
        self.manager.current = 'login'

    def on_daftar_click(self):
        message = "Hallo Aplikasi Pengelola Dana Desa, Saya Ingin Menjadi Admin !!!"
        phone_number = "6282328594802"  # Ganti dengan nomor WhatsApp tujuan
        if platform.system() == 'Windows':
            # Untuk Windows, buka di browser
            webbrowser.open(f"https://wa.me/{phone_number}?text={message}")
        else:
            # Untuk Android dan iOS
            url = f"whatsapp://send?phone={phone_number}&text={message}"
            webbrowser.open(url)  # Ini akan membuka WhatsApp jika terinstal