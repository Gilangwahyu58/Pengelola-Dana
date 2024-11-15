# splash.py
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.lang import Builder

# Muat file KV untuk SplashScreen
Builder.load_file('splash.kv')

class SplashScreen(Screen):
    def on_enter(self):
        # Pindah ke layar beranda 
        Clock.schedule_once(self.go_to_beranda, 15)

    def go_to_beranda(self, dt):
        self.manager.current = 'beranda'  # Ganti dengan nama layar beranda yang sesuai