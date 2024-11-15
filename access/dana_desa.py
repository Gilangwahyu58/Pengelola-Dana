from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.graphics import Color, Line  # Pastikan Anda mengimpor Color dan Line
from database import AdminLogin, Penggunaan  # Pastikan Anda memiliki kelas AdminLogin dan Penggunaan
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.clock import Clock

class DanaDesaScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.total_keuangan = 0  # Inisialisasi total keuangan
        self.keuangan_input_event = None  # Menyimpan event untuk debounce

    def on_enter(self):
        """Method ini dipanggil ketika layar ini ditampilkan."""
        try:
            # Ambil nama desa dari layar login
            self.nama_desa = self.manager.get_screen('login').nama_desa
            self.load_penggunaan_data(self.nama_desa)  # Panggil metode untuk memuat data penggunaan
            self.load_keuangan_data(self.nama_desa)  # Panggil metode untuk memuat data keuangan
            
            # Bind event untuk mengupdate sisa dana saat input keuangan berubah
            
            self.ids.keuangan_input.bind(text=self.on_keuangan_input_change)
        except Exception as e:
            print(f"Error saat memasuki layar: {e}")

    def load_penggunaan_data(self, nama_desa):
        """Memuat data penggunaan dari database dan menampilkannya di UI."""
        try:
            penggunaan_data = Penggunaan.get_penggunaan_data(nama_desa)
            total_penggunaan = sum(item['jumlah'] for item in penggunaan_data)
            self.ids.penggunaan.text = f'Total Penggunaan Dana: Rp {total_penggunaan:,}'

            # Kosongkan widget sebelumnya
            self.ids.usage_list.clear_widgets()
            for item in penggunaan_data:
                penggunaan_label = f"{item['judul']}: Rp {item['jumlah']:,}"
                penggunaan_widget = Label(
                    text=penggunaan_label,
                    font_size=14,
                    color=(0, 0, 0, 1),
                    size_hint_y=None,
                    height=30,
                    halign='left',  # Menentukan perataan horizontal
                    valign='middle',  # Menentukan perataan vertikal
                    text_size=(self.ids.usage_list.width, None)  # Mengatur ukuran teks
                )
                penggunaan_widget.bind(size=lambda *x: penggunaan_widget.setter('text_size')(penggunaan_widget, (penggunaan_widget.width, None)))
                self.ids.usage_list.add_widget(penggunaan_widget)

            # Hitung sisa dana setelah memuat penggunaan
            self.update_sisa_dana()  # Memanggil metode untuk menghitung sisa dana

            # Perbarui tinggi GridLayout sesuai dengan jumlah widget yang ditambahkan
            self.ids.usage_list.height = len(penggunaan_data) * 30  # Sesuaikan dengan tinggi setiap item

            # Tambahkan garis horizontal di bawah GridLayout
            self.draw_horizontal_line()
        except Exception as e:
            print(f"Error saat memuat data penggunaan: {e}")

    def load_keuangan_data(self, nama_desa):
        """Memuat data keuangan dari database."""
        try:
            keuangan_data = Penggunaan.get_keuangan_data(nama_desa)
            if keuangan_data:
                self.total_keuangan = keuangan_data.get('total_keuangan', 0)  # Ambil total keuangan dari Firebase
                self.ids.keuangan_input.text = str(self.total_keuangan)
                self.ids.total_keuangan.text = f'Total Keuangan Desa: Rp {self.total_keuangan:,}'  # Update label
                self.draw_horizontal_line()
            else:
                self.ids.keuangan_input.text = "0"  # Set default jika tidak ada data
                self.ids.total_keuangan.text = 'Total Keuangan Desa: Rp 0'  # Update label
            self.update_sisa_dana()  # Hitung sisa dana saat memuat data keuangan
        except Exception as e:
            print(f"Error saat memuat data keuangan: {e}")

    def on_keuangan_input_change(self, instance, value):
        """Mengupdate sisa dana saat input keuangan berubah."""
        if self.keuangan_input_event:
            self.keuangan_input_event.cancel()  # Batalkan event sebelumnya jika ada
        self.keuangan_input_event = Clock.schedule_once(self.update_sisa_dana, 0.5)  # Tunggu 0.5 detik

    def add_keuangan(self):
        """Menambahkan dana ke total keuangan desa dan menyimpannya ke Firebase."""
        try:
            tambahan_keuangan = int(self.ids.keuangan_input.text)
            if tambahan_keuangan <= 0:
                raise ValueError("Jumlah harus lebih dari 0.")  # Validasi jika jumlah tidak valid
            
            # Simpan ke Firebase
            Penggunaan.save_keuangan_data(self.nama_desa, tambahan_keuangan)  # Simpan ke Firebase
            
            self.total_keuangan += tambahan_keuangan  # Tambahkan ke total
            self.ids.keuangan_input.text = '0'  # Reset input setelah menambah
            self.update_sisa_dana()  # Perbarui sisa dana
            self.show_popup(f"Keuangan desa berhasil ditambahkan: Rp {tambahan_keuangan:,}")
        except ValueError as ve:
            print(f"Input tidak valid: {ve}")
        except Exception as e:
            print(f"Error saat menambahkan keuangan: {e}")
    def update_sisa_dana(self, *args):
        """Menghitung dan memperbarui sisa dana berdasarkan input keuangan dan total penggunaan."""
        try:
            total_penggunaan = sum(item['jumlah'] for item in Penggunaan.get_penggunaan_data(self.nama_desa))
            sisa_dana = self.total_keuangan - total_penggunaan
            self.ids.sisa.text = f'Keuangan Desa yang tersisa: Rp {sisa_dana:,}'
        except ValueError:
            self.ids.sisa.text = 'Keuangan Desa yang tersisa: Rp 0'
    def save_financial_data(self):
        """Menyimpan data keuangan desa ke Firebase."""
        try:
            keuangan_input = int(self.ids.keuangan_input.text)
            Penggunaan.save_keuangan_data(self.nama_desa, keuangan_input)  # Simpan ke Firebase
            self.total_keuangan += keuangan_input  # Update total keuangan lokal
            self.ids.total_keuangan.text = f'Total Keuangan Desa: Rp {self.total_keuangan:,}'  # Update label
            print("Data keuangan berhasil disimpan.")
            self.update_sisa_dana()  # Update sisa dana setelah menyimpan
            self.show_popup("Keuangan desa berhasil diperbarui!")  # Tampilkan popup
        except ValueError:
            print("Input tidak valid, harap masukkan angka.")
        except Exception as e:
            print(f"Error saat menyimpan data keuangan: {e}")

    def draw_horizontal_line(self):
        """Menggambar garis horizontal di bawah GridLayout."""
        with self.ids.usage_list.canvas:
            Color(0, 0, 0, 1)  # Warna garis
            Line(points=[self.ids.usage_list.x, self.ids.usage_list.y, self.ids.usage_list.x + self.ids.usage_list.width, self.ids.usage_list.y], width=1)  # Menggambar garis horizontal
    
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
