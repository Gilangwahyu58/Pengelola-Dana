from kivy.uix.screenmanager import Screen
from kivy.app import App
from database import Penggunaan
from datetime import datetime
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.clock import Clock

class PenggunaanEditScreen(Screen):
    usage_title = ''  # Judul yang akan diedit
    usage_id = ''     # ID dari data yang akan diedit
    dialog = None

    def on_enter(self):
        """Method ini dipanggil ketika layar ini ditampilkan."""
        self.ids.usage_title.text = self.usage_title
        self.ids.usage_description.text = self.get_usage_description()  # Ambil deskripsi dari database
        self.ids.usage_date.text = self.get_usage_date()  # Ambil tanggal dari database
        self.ids.usage_amount.text = str(self.get_usage_amount())  # Ambil jumlah dari database

    def get_usage_description(self):
        """Mendapatkan deskripsi dari database berdasarkan judul."""
        usage_data = Penggunaan.get_penggunaan_data_by_title(self.usage_title)
        return usage_data.get('deskripsi', 'Deskripsi tidak ditemukan') if usage_data else 'Deskripsi tidak ditemukan'

    def get_usage_date(self):
        """Mendapatkan tanggal dari database berdasarkan judul."""
        usage_data = Penggunaan.get_penggunaan_data_by_title(self.usage_title)
        return usage_data.get('tanggal', 'Tanggal tidak ditemukan') if usage_data else 'Tanggal tidak ditemukan'

    def get_usage_amount(self):
        """Mendapatkan jumlah dari database berdasarkan judul."""
        usage_data = Penggunaan.get_penggunaan_data_by_title(self.usage_title)
        return usage_data.get('jumlah', 0) if usage_data else 0

    def edit_usage(self):
        """Method untuk mengedit data penggunaan."""
        judul = self.ids.usage_title.text.strip()
        deskripsi = self.ids.usage_description.text.strip()
        jumlah = self.ids.usage_amount.text.strip()
        tanggal = datetime.now().strftime("%Y-%m-%d")  # Mengambil tanggal hari ini

        if not judul or not deskripsi or not jumlah:
            self.show_popup("Judul, deskripsi, dan jumlah tidak boleh kosong.")
            return

        try:
            # Konversi jumlah ke float
            jumlah = float(jumlah)
            
            # Sebelum mengupdate, cetak nilai yang akan diupdate
            print(f"Updating usage from '{self.usage_title}' to '{judul}' with description '{deskripsi}', amount '{jumlah}', and date '{tanggal}'")
            
            # Mengupdate data berdasarkan judul
            Penggunaan.update_penggunaan_data_by_title(self.usage_title, judul, deskripsi, tanggal, jumlah)
            
            print("Data penggunaan berhasil diperbarui.")
            self.show_popup("Perubahan berhasil disimpan")  # Tampilkan popup
            self.manager.current = 'adm_penggunaan'  # Kembali ke layar adm_penggunaan
        except Exception as e:
            print(f"Error saat memperbarui data: {e}")
            self.show_popup("Terjadi kesalahan saat menyimpan data.")

    def delete_usage(self):
        """Method untuk menghapus data penggunaan berdasarkan judul."""
        judul = self.ids.usage_title.text.strip()  # Ambil judul dari input

        if not judul:
            self.show_popup("Judul tidak boleh kosong.")
            return

        try:
            # Sebelum menghapus, cetak judul yang akan dihapus
            print(f"Deleting usage with title: '{judul}'")
            
            # Panggil metode untuk menghapus data berdasarkan judul
            Penggunaan.delete_penggunaan_by_title(judul)
            
            print("Data penggunaan berhasil dihapus.")
            self.show_popup("Data berhasil dihapus")  # Tampilkan popup
            self.manager.current = 'adm_penggunaan'  # Kembali ke layar adm_penggunaan
        except Exception as e:
            print(f"Error saat menghapus data: {e}")
            self.show_popup("Terjadi kesalahan saat menghapus data.")

    def show_popup(self, message):
        """Menampilkan popup dengan pesan tertentu."""
        dialog_content = MDBoxLayout(orientation='vertical', padding=10, spacing=10)
        
        label = MDLabel(
            text=message,
            theme_text_color='Custom',
            text_color=(1, 1, 1, 1),  # Warna teks 
            font_style='Body2',
            halign='center',
            size_hint_y=None,
            height=20
        )
        dialog_content.add_widget(label)

        self.dialog = MDDialog(
            type='custom',
            content_cls=dialog_content,
            size_hint=(None, None),
            size=(265, 100),
            md_bg_color=[0, 0, 0, 1],
            auto_dismiss=True, 
        )
        
        self.dialog.open()
        self.dialog.pos_hint = {'center_x': 0.5, 'top': 0.99}

        Clock.schedule_once(self.close_dialog, 10)

    def close_dialog(self, dt):
        """Menutup dialog."""
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None