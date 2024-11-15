from kivy.uix.screenmanager import Screen
from kivy.app import App
from database import Penggunaan  # Pastikan Anda memiliki kelas Penggunaan di database.py
from storage import StorageManagerKemajuan
from datetime import datetime
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.button import ButtonBehavior
from kivy.uix.filechooser import FileChooserIconView

class ImageSelectPopup(Popup):
    def __init__(self, on_select, **kwargs):
        super(ImageSelectPopup, self).__init__(**kwargs)
        self.title = "Pilih Gambar"
        self.size_hint = (0.9, 0.9)

        layout = BoxLayout(orientation='vertical')

        # FileChooser untuk memilih gambar
        self.filechooser = FileChooserIconView()
        layout.add_widget(self.filechooser)

        # Tombol untuk memilih gambar
        select_button = Button(text="Pilih Gambar", size_hint_y=None, height=50)
        select_button.bind(on_press=lambda x: self.select_image(on_select))
        layout.add_widget(select_button)

        self.add_widget(layout)

    def select_image(self, on_select):
        selected = self.filechooser.selection
        if selected:
            # Ambil path gambar yang dipilih
            image_path = selected[0]
            print(f"Gambar dipilih: {image_path}")
            on_select(image_path)  # Panggil callback untuk mengupdate gambar
            self.dismiss()  # Menutup popup setelah memilih gambar

class KemajuanEditScreen(Screen):
    usage_title = ''  # Judul yang akan diedit
    dialog = None

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
            print("Available IDs:", self.ids)
            
            self.ids.usage_description.text = usage_data.get('deskripsiKemajuan', 'Deskripsi tidak ditemukan')
            self.ids.usage_date.text = usage_data.get('tanggal', 'Tanggal tidak ditemukan')
            self.ids.usage_amount.text = str(usage_data.get('jumlah', 0))
            self.ids.usage_percentage.text = f"{usage_data.get('persentase', 0)}%"
            self.ids.progress_image.source = usage_data.get('gambar', '')
        else:
            print("Tidak ada data yang ditemukan untuk judul:", self.usage_title)

    def update_image_source(self, image_path):
        """Mengupdate sumber gambar dan mengunggahnya ke storage."""
        self.ids.progress_image.source = image_path
        self.ids.progress_image.reload()  # Reload image to show the new one

        # Panggil fungsi untuk mengunggah gambar menggunakan StorageManagerKemajuan
        upload_result = StorageManagerKemajuan.upload_profile_image(image_path)  # Menggunakan metode upload_image
        if upload_result['status'] == "success":
            print(f"Gambar berhasil diunggah: {upload_result['url']}")
            self.save_image_path(upload_result['url'])  # Simpan URL jika berhasil
        else:
            print("Gagal mengunggah gambar:", upload_result['message'])

    def save_image_path(self, image_path):
        """Method to save the image path to the database."""
        try:
            # Update the usage data in the database
            Penggunaan.update_image_path_by_title(self.usage_title, image_path)  # Ensure this method exists
            print("Image path successfully saved to the database.")
        except Exception as e:
            print(f"Error saat menyimpan path gambar: {e}")
    def clear_image(self):
        """Menghapus gambar yang ditampilkan dan memperbarui database."""
        self.ids.progress_image.source = ''  # Menghapus sumber gambar
        print("Gambar dihapus.")

        # Panggil fungsi untuk menghapus gambar dari storage jika diperlukan
        # Misalnya, jika Anda menyimpan URL gambar di database, Anda bisa menghapusnya
        try:
            Penggunaan.update_image_path_by_title(self.usage_title, '')  # Menghapus path gambar di database
            print("Path gambar berhasil dihapus dari database.")
        except Exception as e:
            print(f"Error saat menghapus path gambar: {e}")
    def edit_usage(self):
        """Method untuk mengedit data kemajuan."""
        judul = self.ids.usage_title.text.strip()
        deskripsi = self.ids.usage_description.text.strip()
        jumlah = self.ids.usage_amount.text.strip()
        tanggal = datetime.now().strftime("%Y-%m-%d")  # Mengambil tanggal hari ini
        presentase = self.ids.usage_percentage.text.strip()  # Mengambil presentase dari TextInput
        gambar = self.ids.progress_image.source  # Mengambil sumber gambar dari Image

        if not judul or not deskripsi or not jumlah:
            self.show_popup("Judul, deskripsi, dan jumlah tidak boleh kosong.")
            return

        try:
            # Konversi jumlah ke float
            jumlah = float(jumlah)
            presentase = float(presentase.strip('%'))  # Konversi presentase ke float

            # Sebelum mengupdate, cetak nilai yang akan diupdate
            print(f"Updating kemajuan from '{self.usage_title}' to '{judul}' with description '{deskripsi}', amount '{jumlah}', percentage '{presentase}', and date '{tanggal}'")
            
            # Mengupdate data berdasarkan judul
            Penggunaan.update_kemajuan_data_by_title(self.usage_title, judul, deskripsi, tanggal, jumlah, presentase, gambar)
            
            print("Data kemajuan berhasil diperbarui.")
            self.show_popup("Perubahan berhasil disimpan")  # Tampilkan popup
            self.manager.current = 'adm_kemajuan'  # Kembali ke layar adm_kemajuan
        except Exception as e:
            print(f"Error saat memperbarui data: {e}")
            self.show_popup("Terjadi kesalahan saat menyimpan data.")

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
        self.dialog.pos_hint = {'center_x':  0.5, 'top': 0.99}

        Clock.schedule_once(self.close_dialog, 10)

    def close_dialog(self, dt):
        """Menutup dialog."""
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None

    def open_image_selector(self):
        """Membuka popup untuk memilih gambar."""
        popup = ImageSelectPopup(on_select=self.update_image_source)
        popup.open()

    def update_image_source(self, image_path):
        """Update image source and upload to storage."""
        self.ids.progress_image.source = image_path
        self.ids.progress_image.reload()  # Reload image to show the new one

        # Upload image using StorageManagerKemajuan
        upload_result = StorageManagerKemajuan.upload_profile_image(image_path)  # Use the upload method
        if upload_result['status'] == "success":
            print(f"Image uploaded successfully: {upload_result['url']}")
            self.save_image_path(upload_result['url'])  # Save URL if successful
        else:
            print("Failed to upload image:", upload_result['message'])