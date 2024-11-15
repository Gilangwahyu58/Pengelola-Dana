from kivy.uix.screenmanager import Screen
from database import Anggota  # Pastikan Anda mengimpor kelas Anggota dari database.py

class UserAnggotaScreen(Screen):
    anggota_id = None 

    def on_enter(self):
        self.load_anggota()

    def load_anggota(self):
        if self.anggota_id is not None:
            anggota_data = Anggota.get_anggota(self.anggota_id)  # Mengambil data anggota dari database
            print(f"Data anggota yang diambil: {anggota_data}")  # Debugging line
            if anggota_data:
                # Memuat data ke Label
                self.ids.nama_label.text = str(anggota_data.get('nama', ''))
                self.ids.jabatan_label.text = str(anggota_data.get('jabatan', ''))
                self.ids.masa_periode_label.text = str(anggota_data.get('masaPeriode', ''))
                self.ids.no_telp_label.text = str(anggota_data.get('noTelp', ''))