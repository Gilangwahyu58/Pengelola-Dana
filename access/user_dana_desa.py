from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.graphics import Color, Line
from database import AdminLogin, Penggunaan  # Pastikan Anda memiliki kelas AdminLogin dan Penggunaan

class UserDanaDesaScreen(Screen):
    def on_enter(self):
        """Method ini dipanggil ketika layar ini ditampilkan."""
        try:
            # Ambil nama desa dari layar login
            self.nama_desa = self.manager.get_screen('login').nama_desa
            self.load_penggunaan_data(self.nama_desa)  # Panggil metode untuk memuat data penggunaan
            self.load_keuangan_data(self.nama_desa)  # Panggil metode untuk memuat data keuangan
            
            # Bind event untuk mengupdate sisa dana saat input keuangan berubah
            self.ids.keuangan_input.bind(on_text_validate=self.update_sisa_dana)
            self.ids.keuangan_input.bind(text=self.update_sisa_dana)

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
                    halign='left',
                    valign='middle',
                    text_size=(self.ids.usage_list.width, None)
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
            total_keuangan = keuangan_data.get('financial_amount', 0) if keuangan_data else 0
            self.ids.keuangan_input.text = f'Total Keuangan Desa: Rp {total_keuangan:,}'  # Memperbarui teks label
            self.update_sisa_dana()  # Hitung sisa dana saat memuat data keuangan
        except Exception as e:
            print(f"Error saat memuat data keuangan: {e}")

    def update_sisa_dana(self, *args):
        """Menghitung dan memperbarui sisa dana berdasarkan input keuangan dan total penggunaan."""
        try:
            total_penggunaan = sum(item['jumlah'] for item in Penggunaan.get_penggunaan_data(self.nama_desa))
            # Ambil nominal dari label keuangan_input
            keuangan_input = int(self.ids.keuangan_input.text.split("Rp ")[1].replace(",", "").strip()) if "Rp" in self.ids.keuangan_input.text else 0
            sisa_dana = keuangan_input - total_penggunaan
            self.ids.sisa.text = f'Keuangan desa yang tersisa: Rp {sisa_dana:,}'
        except (ValueError, IndexError):
            self.ids.sisa.text = 'Keuangan desa yang tersisa: Rp 0'  # Reset jika input tidak valid
            print("Input keuangan tidak valid.")

    def save_financial_data(self):
        """Menyimpan data keuangan desa ke Firebase."""
        try:
            keuangan_input = int(self.ids.keuangan_input.text)
            Penggunaan.save_keuangan_data(self.nama_desa, keuangan_input)  # Simpan ke Firebase
            print("Data keuangan berhasil disimpan.")
            self.update_sisa_dana()  # Update sisa dana setelah menyimpan
        except ValueError :
            print("Input tidak valid, harap masukkan angka.")
        except Exception as e:
            print(f"Error saat menyimpan data keuangan: {e}")

    def draw_horizontal_line(self):
        """Menggambar garis horizontal di bawah GridLayout."""
        with self.ids.usage_list.canvas:
            Color(0, 0, 0, 1)  # Warna garis
            Line(points=[self.ids.usage_list.x, self.ids.usage_list.y, self.ids.usage_list.x + self.ids.usage_list.width, self.ids.usage_list.y], width=1)  # Menggambar garis horizontal