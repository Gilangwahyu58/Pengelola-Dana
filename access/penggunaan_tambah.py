from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from datetime import datetime
from database import Penggunaan  # Pastikan Anda mengimpor kelas Penggunaan

class PenggunaanTambahScreen(Screen):
    def __init__(self, nama_desa=None, **kwargs):
        super(PenggunaanTambahScreen, self).__init__(**kwargs)
        self.nama_desa = nama_desa or "Desa Tidak Diketahui"  # Atur nilai default jika tidak ada nama desa
        self.dialog = None  # Inisialisasi dialog

    def on_pre_leave(self):
        """Method ini dipanggil sebelum layar ditutup."""
        # Kosongkan semua inputan
        self.ids.usage_title_input.text = ""
        self.ids.usage_description_input.text = ""
        self.ids.usage_amount_input.text = ""
    def tambah_usage(self, instance):
        # Logika untuk menambahkan data penggunaan ke database
        judul = self.ids.usage_title_input.text.strip()  # Menggunakan ID dari .kv
        deskripsi = self.ids.usage_description_input.text.strip()  # Menggunakan ID dari .kv
        jumlah = self.ids.usage_amount_input.text.strip()  # Mengambil jumlah dari input
        tanggal = datetime.now().strftime("%Y-%m-%d")  # Mendapatkan tanggal saat ini

        if judul and deskripsi and jumlah:
            try:
                # Konversi jumlah ke float
                jumlah = float(jumlah)  # Pastikan jumlah adalah angka
                # Panggil metode untuk menambahkan data penggunaan
                Penggunaan.add_penggunaan_data(self.nama_desa, judul, deskripsi, tanggal, jumlah)
                # Tampilkan popup untuk konfirmasi
                self.show_dialog("Sukses","Data penggunaan berhasil ditambahkan.")
                self.ids.usage_title_input.text = ""  # Kosongkan field judul
                self.ids.usage_description_input.text = ""  # Kosongkan field deskripsi
                self.ids.usage_amount_input.text = ""  # Kosongkan field jumlah
            except Exception as e:
                # Tampilkan popup jika terjadi kesalahan saat menambahkan data
                self.show_dialog("Error", f"Terjadi kesalahan: {str(e)}")
        else:
            self.show_dialog("Warning", "Judul, keterangan, dan jumlah tidak boleh kosong.")

    def show_dialog(self, title, message):
        """Menampilkan dialog dengan pesan tertentu."""
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
            title=title,
            type='custom',
            content_cls=dialog_content,
            size_hint=(None, None),
            size=(265, 100),
            md_bg_color=[0, 0, 0, 1],
            auto_dismiss=True, 
        )
        
        self.dialog.open()
        self.dialog.pos_hint = {'center_x': 0.5, 'top': 0.99}

        # Menutup dialog setelah 2 detik
        Clock.schedule_once(self.close_dialog, 10)

    def close_dialog(self, dt):
        """Menutup dialog."""
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None