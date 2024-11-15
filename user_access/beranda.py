from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel 

class BerandaScreen(Screen):
    def on_kv_post(self, base_widget):
        grid_layout = self.ids.anggota_grid
        for i in range(5):
            anggota = AnggotaWidget(i)
            anggota.bind(on_press=lambda instance, index=i: self.show_notification(index))
            grid_layout.add_widget(anggota)

    def show_notification(self, index):
        print(f'Anda mengklik anggota {index + 1}.')
        self.show_popup_login_required()

    def show_popup_login_required(self):
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

class AnggotaWidget(BoxLayout):
    def __init__(self, index, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 5
        self.spacing = 2
        self.size_hint_y = None
        self.height = 80
        image = Image(
            source=f'assets/image/anggota_{index + 1}.png',
            allow_stretch=True,
            size_hint_y=None,
            height=30
        )
        label = Label(
            text=f'Anggota {index + 1}',
            font_size=12,
            size_hint_y=None,
            height=20,
            color=(0, 0, 0, 1)
        )
        self.add_widget(image)
        self.add_widget(label)
        self.index = index

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            app = MDApp.get_running_app()
            screen = app.root.get_screen('beranda')
            screen.show_notification(self.index)
            return True
        return super().on_touch_down(touch)