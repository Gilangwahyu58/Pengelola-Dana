from kivy.uix.screenmanager import Screen
from kivy.app import App
from database import Penggunaan  # Pastikan Anda memiliki kelas Penggunaan di database.py
from kivymd.uix.label import MDLabel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView

class UserPenggunaanScreen(Screen):
    usage_title = ''  # Pastikan Anda memiliki atribut ini

    def on_enter(self):
        """Method ini dipanggil ketika layar ini ditampilkan."""
        self.ids.usage_title.text = self.usage_title
        self.ids.usage_description.text = self.get_usage_description()  # Ambil deskripsi dari database
        self.ids.usage_date.text = f"Tanggal: {self.get_usage_date()}"  # Ambil tanggal dari database
        self.ids.usage_amount.text = f"Dana Yang Diperlukan: Rp {self.get_usage_amount():,}"  # Ambil jumlah dari database

    def get_usage_description(self):
        """Mendapatkan deskripsi dari database berdasarkan judul."""
        usage_data = Penggunaan.get_penggunaan_data_by_title(self.usage_title)
        return usage_data.get('deskripsi', 'Deskripsi tidak ditemukan') if usage_data else 'Deskripsi tidak ditemukan'

    def get_usage_date(self):
        """Mendapatkan tanggal dari database berdasarkan judul."""
        usage_data = Penggunaan.get_penggunaan_data_by_title(self.usage_title)
        
        if usage_data:
            # Jika data ditemukan, update label dan kembalikan tanggal
            tanggal = usage_data.get('tanggal', 'Tanggal tidak ditemukan')
            self.ids.usage_date.text = f"Tanggal: {tanggal}"
            return tanggal
        else:
            # Jika tidak ditemukan, update label dan kembalikan pesan default
            self.ids.usage_date.text = "Tanggal tidak ditemukan"
            return 'Tanggal tidak ditemukan'

    def get_usage_amount(self):
        """Mendapatkan jumlah dari database berdasarkan judul."""
        usage_data = Penggunaan.get_penggunaan_data_by_title(self.usage_title)
        
        if usage_data:
            # Jika data ditemukan, update label dan kembalikan jumlah
            jumlah = usage_data.get('jumlah', 0)
            self.ids.usage_amount.text = f"Dana Yang Diperlukan: Rp {jumlah:,}"
            return jumlah
        else:
            # Jika tidak ditemukan, update label dan kembalikan nilai default
            self.ids.usage_amount.text = "Dana tidak ditemukan"
            return 0