import webbrowser
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.app import App
from database import AdminLogin
from database import Anggota

class AdmAnggotaWidget(BoxLayout):
    def __init__(self, index, anggota_id, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 5
        self.spacing = 2
        self.size_hint_y = None
        self.height = 80

        self.index = index
        self.anggota_id = anggota_id
        
        image_path = f'assets/image/anggota_1.png'
        print(f'Loading image from: {image_path}')  # Debugging line
        
        self.image = Image(
            source=image_path,
            allow_stretch=True,
            size_hint_y=None,
            height=30
        )
        
        self.label = Label(
            text=f'Anggota {index + 1}',
            font_size=12,
            size_hint_y=None,
            height=20,
            color=(0, 0, 0, 1)
        )
        
        self.add_widget(self.image)
        self.add_widget(self.label)

        # Bind the click event to the on_click method
        self.bind(on_touch_down=self.on_click)

    def on_click(self, instance, touch):
        if self.collide_point(touch.x, touch.y):
            app = App.get_running_app()
            screen = app.root.get_screen('adm_beranda')
            screen.go_to_anggota(self.anggota_id) 
            return True  # Indicate that the touch event has been handled
        return super().on_touch_down(touch)

class AdmBerandaScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nama_desa = None  # Initialize nama_desa

    def on_enter(self):  # This method is called when the screen is entered
        app = App.get_running_app()
        self.nama_desa = app.root.get_screen('login').nama_desa
        self.load_anggota()
    
    def load_anggota(self):
        grid_layout = self.ids.anggota_grid
        grid_layout.clear_widgets()

        anggota_list = Anggota.get_anggota_by_desa(self.nama_desa)

        jabatan_order = [
            'kepala desa',
            'sekretaris',
            'bendahara',
            'admin',
            'seksi',
            'lainnya'
        ]

        # Create a dictionary to hold anggota by their positions
        anggota_by_jabatan = {jabatan: [] for jabatan in jabatan_order}

        # Organize anggota by their positions
        for anggota_id, anggota_data in anggota_list:
            jabatan = anggota_data.get('jabatan', '').lower()  # Get the jabatan and convert to lowercase
            for position in jabatan_order:
                if position in jabatan:  # Check if the position is in the jabatan
                    anggota_by_jabatan[position].append((anggota_id, anggota_data))
                    break  # Stop checking once we find the matching position

        # Add anggota to the grid layout in the defined order
        for position in jabatan_order:
            for anggota_id, anggota_data in anggota_by_jabatan[position]:
                anggota_widget = AdmAnggotaWidget(len(grid_layout.children), anggota_id)  # Pass anggota_id here
                anggota_widget.label.text = anggota_data.get('nama', 'Nama Tidak Diketahui')
                grid_layout.add_widget(anggota_widget)

        # Add button to add member
        button_tambah = Button(
            text='+', 
            size_hint_y=None, 
            height=60, 
            background_color=(0, 0, 0, 0),
            color=(0, 0, 0, 1), 
            font_size='40sp', 
            bold=True, 
            on_press=self.on_button_tambah_press
        )
        grid_layout.add_widget(button_tambah)

    def on_button_tambah_press(self, instance):
        app = App.get_running_app()
        self.manager.current = 'anggotatb'

    def go_to_anggota(self, anggota_id):
        print(f'Anda mengklik anggota dengan ID {anggota_id}.')
        app = App.get_running_app()
        anggota_screen = app.root.get_screen('anggota')
        anggota_screen.anggota_id = anggota_id  # Set the anggota_id in `AnggotaScreen`
        anggota_screen.load_anggota()  # Load the member data
        self.manager.current = 'anggota'
    def on_image_click(self):
        # Fetch the map link from the database
        map_link = self.get_map_link_from_db(self.nama_desa)
        
        if map_link:
            # Open the map link in a web browser
            webbrowser.open(map_link)
        else:
            print("Map link not found for the selected village.")

    def get_map_link_from_db(self, nama_desa):
        """Fetch the map link from Firebase."""
        try:
            # Fetch the map link from Firebase
            map_link = AdminLogin.db.child("maps").child(nama_desa).get().val()
            return map_link.get('link') if map_link else None  # Assuming 'link' is the key for the URL
        except Exception as e:
            print(f"Error retrieving map link: {e}")
            return None