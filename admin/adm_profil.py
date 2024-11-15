from kivy.uix.screenmanager import Screen
from database import AdminLogin

class AdmProfileScreen(Screen):
    def __init__(self, **kwargs):
        super(AdmProfileScreen, self).__init__(**kwargs)
        self.nama_pengguna = "Default User"  # Nama pengguna default

    def on_enter(self):
        """Method ini dipanggil ketika layar ini ditampilkan."""
        try:
            # Ambil nama pengguna dari layar login
            self.nama_pengguna = self.manager.get_screen('login').nama_pengguna
            
            # Ambil data pengguna dari AdminLogin
            user_data = AdminLogin.db.child("login").order_by_child("namaPengguna").equal_to(self.nama_pengguna).get()

            if user_data.each():
                for user in user_data.each():
                    self.ids.nama.text = user.val().get('username', 'Nama tidak ditemukan')
                    self.ids.foto_profil.source = user.val().get('fotoProfil', 'assets/image/orang.png')  # Ganti dengan foto profil default jika tidak ada
            else:
                self.ids.nama.text = 'Data tidak ditemukan'
                self.ids.foto_profil.source = 'assets/image/orang.png'  # Set foto profil default jika tidak ada data

        except Exception as e:
            print(f"Error: {e}")
            self.ids.nama.text = 'Error dalam mengambil data'
            self.ids.foto_profil.source = 'assets/image/orang.png'  # Set foto profil default jika terjadi error

    def update_profile_picture(self, new_picture_path):
        """Method untuk memperbarui foto profil."""
        try:
            # Ambil nama pengguna yang sedang login
            nama_pengguna = self.manager.get_screen('login').nama_pengguna
            
            # Update foto profil di database
            user_data = AdminLogin.db.child("login").order_by_child("namaPengguna").equal_to(nama_pengguna).get()
            
            if user_data.each():
                for user in user_data.each():
                    AdminLogin.db.child("login").child(user.key()).update({"fotoProfil": new_picture_path})
                    self.ids.foto_profil.source = new_picture_path  # Update foto profil di UI
            else:
                print("Pengguna tidak ditemukan saat memperbarui foto profil.")
        
        except Exception as e:
            print(f"Error saat memperbarui foto profil: {e}")