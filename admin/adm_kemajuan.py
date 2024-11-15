from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App
from database import Penggunaan  # Pastikan untuk mengimpor kelas yang sesuai

class AdmKemajuanScreen(Screen):
    def __init__(self, **kwargs):
        super(AdmKemajuanScreen, self).__init__(**kwargs)
        self.nama_desa = "Default User"  # Inisialisasi atribut

    def on_enter(self):
        """Method ini dipanggil ketika layar ini ditampilkan."""
        try:
            # Ambil nama desa dari layar login
            self.nama_desa = self.manager.get_screen('login').nama_desa
            self.load_kemajuan_data(self.nama_desa)  # Panggil metode untuk memuat data kemajuan
        except Exception as e:
            print(f"Error saat memasuki layar: {e}")

    def load_kemajuan_data(self, nama_desa):
        """Mengambil data kemajuan dari database dan menampilkannya."""
        try:
            # Mengambil data kemajuan dari database
            kemajuan_data = Penggunaan.get_penggunaan_data(nama_desa)

            # Debug: Pastikan data yang diambil
            print(f"Data kemajuan untuk {nama_desa}: {kemajuan_data}")

            # Mengosongkan tampilan sebelumnya
            self.ids.kemajuan_list.clear_widgets()

            # Jika tidak ada data, tampilkan pesan
            if not kemajuan_data:
                self.ids.kemajuan_list.add_widget(Label(text="Tidak ada data kemajuan."))
                self.ids.total_penggunaan_label.text = "Total Penggunaan Dana: Rp 0"
                return

            # Menghitung total penggunaan dana
            total_penggunaan = sum(data.get('jumlah', 0) for data in kemajuan_data)  # Ganti 'jumlah' dengan kunci yang sesuai

            # Menampilkan total penggunaan dana
            self.ids.total_penggunaan_label.text = f"Total Penggunaan Dana: Rp {total_penggunaan:,}"

            # Menambahkan data kemajuan ke tampilan
            for kemajuan in kemajuan_data:
                print(f"Kemajuan yang ditemukan: {kemajuan}")  # Debugging output
                
                # Mengambil hanya judul kemajuan
                judul = kemajuan.get('judul', 'Tanpa Judul')  # Jika judul tidak ada, gunakan 'Tanpa Judul'
                
                button = Button(
                    text=judul,  # Hanya menampilkan judul
                    size_hint_y=None,
                    height=30,
                    background_color=(0.529, 0.808, 0.922, 1)
                )
                button.bind(on_release=self.open_edit_screen)
                self.ids.kemajuan_list.add_widget(button)

        except Exception as e:
            print(f"Error saat memuat data kemajuan: {e}")
            self.ids.kemajuan_list.add_widget(Label(text="Error dalam mengambil data kemajuan."))
            self.ids.total_penggunaan_label.text = "Total Penggunaan Dana: Rp 0"

    def open_edit_screen(self, button):
        """Logika untuk membuka layar edit dengan judul yang sesuai."""
        app = App.get_running_app()
        app.root.get_screen('kemajuan_edit').usage_title = button.text
        app.root.current = 'kemajuan_edit'