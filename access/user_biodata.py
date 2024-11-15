from kivy.uix.screenmanager import Screen
from database import AdminLogin  # Pastikan Anda mengimpor modul yang benar

class UserBiodataScreen(Screen):
    def on_enter(self):
        """Method ini dipanggil ketika layar ini ditampilkan."""
        try:
            # Ambil nama pengguna dari layar login
            nama_pengguna = self.manager.get_screen('login').nama_pengguna
            
            # Ambil data pengguna dari AdminLogin
            user_data = AdminLogin.db.child("login").order_by_child("namaPengguna").equal_to(nama_pengguna).get()

            if user_data.each():
                for user in user_data.each():
                    # Ambil data dan masukkan ke dalam label
                    self.ids.nama_lengkap.text = f'[b]Nama Lengkap:[/b]\n{user.val().get("namaLengkap", "Tidak Ditemukan")}'
                    self.ids.nama_desa.text = f'[b]Desa Anda:[/b]\n{user.val().get("namaDesa", "Tidak Ditemukan")}'
                    self.ids.nik.text = f'[b]NIK:[/b]\n{user.val().get("nik", "Tidak Ditemukan")}'
                    self.ids.no_kk.text = f'[b]No.KK:[/b]\n{user.val().get("noKK", "Tidak Ditemukan")}'
            else:
                # Jika tidak ada data
                self.ids.nama_lengkap.text = '[b]Nama Lengkap:[/b]\nTidak Ditemukan'
                self.ids.nama_desa.text = '[b]Desa Anda:[/b]\nTidak Ditemukan'
                self.ids.nik.text = '[b]NIK:[/b]\nTidak Ditemukan'
                self.ids.no_kk.text = '[b]No.KK:[/b]\nTidak Ditemukan'
                
        except Exception as e:
            print(f"Error: {e}")
            self.ids.nama_lengkap.text = '[b]Nama Lengkap:[/b]\nError dalam mengambil data'
            self.ids.nama_desa.text = '[b]Desa Anda:[/b]\nError dalam mengambil data'
            self.ids.nik.text = '[b]NIK:[/b]\nError dalam mengambil data'
            self.ids.no_kk.text = '[b]No.KK:[/b]\nError dalam mengambil data'