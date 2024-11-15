from kivy.uix.screenmanager import Screen
from kivy.app import App
from database import Penggunaan  # Pastikan Anda memiliki kelas Penggunaan di database.py
from kivymd.uix.label import MDLabel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView

class UserKemajuanScreen(Screen):
    def on_enter(self):
        """Method ini dipanggil ketika layar ini ditampilkan."""
        self.ids.usage_title.text = self.usage_title
        self.load_usage_data()  # Panggil fungsi untuk memuat data


    def load_usage_data(self):
        """Memuat data kemajuan dari database."""
        usage_data = Penggunaan.get_kemajuan_data_by_title(self.usage_title)

        if usage_data:
            # Debugging output
            print(f"Data yang diambil: {usage_data}")
            
            self.ids.usage_description.text = usage_data.get('deskripsiKemajuan', 'Deskripsi tidak ditemukan')
            self.ids.usage_date.text = f"Tanggal: {usage_data.get('tanggal', 'Tanggal tidak ditemukan')}"
            self.ids.usage_amount.text = f"Dana Yang Diperlukan: {str(usage_data.get('jumlah', 0))}"
            self.ids.usage_percentage.text = f"Persentase Kemajuan: {usage_data.get('persentase', 0)}%"
            self.ids.progress_image.source = usage_data.get('gambar', '')
        else:
            print("Tidak ada data yang ditemukan untuk judul:", self.usage_title)