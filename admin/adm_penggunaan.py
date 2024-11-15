from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App
from database import Penggunaan

class AdmPenggunaanScreen(Screen):
    def __init__(self, **kwargs):
        super(AdmPenggunaanScreen, self).__init__(**kwargs)
        self.nama_desa = "Default User"  # Inisialisasi atribut

    def on_enter(self):
        """Method ini dipanggil ketika layar ini ditampilkan."""
        try:
            # Ambil nama desa dari layar login
            self.nama_desa = self.manager.get_screen('login').nama_desa
            self.load_penggunaan_data(self.nama_desa)  # Panggil metode untuk memuat data penggunaan
        except Exception as e:
            print(f"Error saat memasuki layar: {e}")

    def load_penggunaan_data(self, nama_desa):
        """Mengambil data penggunaan dari database dan menampilkannya."""
        try:
            # Mengambil data penggunaan dari database
            penggunaan_data = Penggunaan.get_penggunaan_data(nama_desa)

            # Debug: Pastikan data yang diambil
            print(f"Data penggunaan untuk {nama_desa}: {penggunaan_data}")

            # Mengosongkan tampilan sebelumnya
            self.ids.penggunaan_list.clear_widgets()

            # Jika tidak ada data, tampilkan pesan
            if not penggunaan_data:
                self.ids.penggunaan_list.add_widget(Label(text="Tidak ada data penggunaan."))
                self.ids.total_penggunaan_label.text = "Total Penggunaan Dana: Rp 0"
                return

            # Menghitung total penggunaan dana
            total_penggunaan = sum(data.get('jumlah', 0) for data in penggunaan_data)  # Ganti 'jumlah' dengan kunci yang sesuai

            # Menampilkan total penggunaan dana
            self.ids.total_penggunaan_label.text = f"Total Penggunaan Dana: Rp {total_penggunaan:,}"

            # Menambahkan data penggunaan ke tampilan
            for penggunaan in penggunaan_data:
                # Membuat tombol untuk setiap kegiatan
                button = Button(
                    text=penggunaan['judul'],
                    size_hint_y=None,
                    height=30,
                    background_color=(0.529, 0.808, 0.922, 1)                    
                )
                
                button.bind(on_release=self.open_edit_screen)  # Menghubungkan klik tombol ke metode
                self.ids.penggunaan_list.add_widget(button)

        except Exception as e:
            print(f"Error saat memuat data penggunaan: {e}")
            self.ids.penggunaan_list.add_widget(Label(text="Error dalam mengambil data penggunaan."))
            self.ids.total_penggunaan_label.text = "Total Penggunaan Dana: Rp 0"

    def open_edit_screen(self, button):
        """Logika untuk membuka layar edit dengan judul yang sesuai."""
        app = App.get_running_app()
        app.root.get_screen('penggunaan_edit').usage_title = button.text
        app.root.current = 'penggunaan_edit'

    def add_penggunaan(self):
        """Logika untuk menambah penggunaan."""
        self.manager.current = 'penggunaan_tambah'