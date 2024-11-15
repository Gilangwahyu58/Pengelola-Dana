from kivy.uix.screenmanager import Screen
from kivy.clock import Clock  # Tambahkan import untuk Clock
from kivymd.uix.dialog import MDDialog  # Import MDDialog dari KivyMD
from kivymd.uix.label import MDLabel  # Import MDLabel dari KivyMD
from kivymd.uix.boxlayout import MDBoxLayout  # Import MDBoxLayout dari KivyMD
from database import Anggota  # Pastikan Anda mengimpor kelas Anggota dari database.py

class AnggotaScreen(Screen):
    anggota_id = None  # Menyimpan ID anggota yang sedang diedit
    dialog = None  # Menyimpan instance dialog

    def on_enter(self):
        self.load_anggota()

    def load_anggota(self):
        if self.anggota_id is not None:
            anggota_data = Anggota.get_anggota(self.anggota_id)  # Mengambil data anggota dari database
            print(f"Data anggota yang diambil: {anggota_data}")  # Debugging line
            if anggota_data:
                self.ids.nama_input.text = str(anggota_data.get('nama', ''))
                self.ids.jabatan_input.text = str(anggota_data.get('jabatan', ''))
                self.ids.masa_periode_input.text = str(anggota_data.get('masaPeriode', ''))  # Pastikan nama kunci sesuai
                self.ids.no_telp_input.text = str(anggota_data.get('noTelp', ''))  # Pastikan nama kunci sesuai

    def hapus_anggota(self):
        if self.anggota_id is not None:
            try:
                Anggota.delete_anggota(self.anggota_id)  # Hapus anggota dari database
                # Reset input fields
                self.ids.nama_input.text = ''
                self.ids.jabatan_input.text = ''
                self.ids.masa_periode_input.text = ''
                self.ids.no_telp_input.text = ''
                print(f"Anggota dengan ID {self.anggota_id} telah dihapus.")
                self.show_notification("Anggota berhasil dihapus!")  # Tampilkan notifikasi
            except Exception as e:
                print(f"Error saat menghapus anggota: {e}")
                self.show_notification("Gagal menghapus anggota. Silakan coba lagi.")  # Tampilkan notifikasi error

    def ubah_anggota(self):
        if self.anggota_id is not None:
            anggota_data = {
                'nama': self.ids.nama_input.text,
                'jabatan': self.ids.jabatan_input.text,
                'masaPeriode': self.ids.masa_periode_input.text,  # Pastikan nama kunci sesuai
                'noTelp': self.ids.no_telp_input.text  # Pastikan nama kunci sesuai
            }
            try:
                Anggota.update_anggota(self.anggota_id, anggota_data)  # Perbarui anggota di database
                print(f"Data anggota dengan ID {self.anggota_id} telah diperbarui.")
                self.show_notification("Anggota berhasil diperbarui!")  # Tampilkan notifikasi
            except Exception as e:
                print(f"Error saat memperbarui anggota: {e}")
                self.show_notification("Gagal memperbarui anggota. Silakan coba lagi.")  # Tampilkan notifikasi error

    def show_notification(self, message):
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