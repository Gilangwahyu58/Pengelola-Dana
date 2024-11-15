import pyrebase
import os
from config import get_firebase_config

class AdminLogin:
    config = get_firebase_config()
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    storage = firebase.storage()

    @staticmethod
    def authenticate_user(username, kata_sandi):
        try:
            users = AdminLogin.db.child("login").get()
            if users.each():
                for user in users.each():
                    user_data = user.val()
                    if isinstance(user_data, dict):
                        if user_data.get('username') == username and user_data.get('kataSandi') == kata_sandi:
                            return user_data  # Mengembalikan data pengguna jika login berhasil
            return None  # Login gagal
        except Exception as e:
            print(f"Error authenticating user: {e}")
            return None
    @staticmethod
    def is_nama_pengguna_unik(username):
        """Memeriksa apakah nama pengguna unik."""
        users = AdminLogin.db.child("login").order_by_child("username").equal_to(username).get()
        return not users.each()  # Mengembalikan True jika tidak ada pengguna dengan nama tersebut
    @staticmethod
    def add_user(username, other_data):
        """Menambahkan pengguna baru jika nama pengguna unik."""
        if AdminLogin.is_nama_pengguna_unik(username):
            AdminLogin.db.child("login").push({"username": username, **other_data})
            return True
        else:
            print("Nama pengguna sudah ada. Silakan pilih yang lain.")
            return False
    @staticmethod
    def delete_akun(nama_pengguna):
        """Menghapus akun berdasarkan nama pengguna."""
        try:
            # Pastikan nama_pengguna tidak kosong
            if not nama_pengguna:
                print("Nama pengguna tidak boleh kosong.")
                return False

            # Mencari pengguna berdasarkan nama_pengguna
            users = AdminLogin.db.child("login").order_by_child("namaPengguna").equal_to(nama_pengguna).get()
            
            # Cek apakah ada pengguna yang ditemukan
            if users.each():
                for user in users.each():
                    # Menghapus pengguna berdasarkan key
                    AdminLogin.db.child("login").child(user.key()).remove()
                    print(f"Akun {nama_pengguna} berhasil dihapus.")
                return True
            else:
                print("Akun tidak ditemukan.")
                return False
        except Exception as e:
            print(f"Error deleting akun: {e}")
            return False
    @staticmethod
    def update_nama_pengguna(nama_pengguna_lama, nama_pengguna_baru):
        """Mengupdate nama pengguna di database."""
        try:
            users = AdminLogin.db.child("login").order_by_child("namaPengguna").equal_to(nama_pengguna_lama).get()
            if users.each():
                for user in users.each():
                    AdminLogin.db.child("login").child(user.key()).update({"namaPengguna": nama_pengguna_baru})
                    print(f"Nama pengguna berhasil diupdate dari {nama_pengguna_lama} ke {nama_pengguna_baru}.")
                    return True
            else:
                print("Data pengguna tidak ditemukan.")
                return False
        except Exception as e:
            print(f"Error updating nama pengguna: {e}")
            return False
    @staticmethod
    def get_user_detail(user_id):
        try:
            # Mengakses jalur yang benar
            user_data = AdminLogin.db.child("login").child(user_id).get()
            if user_data.each():
                return user_data.val()
            else:
                print(f"Data pengguna dengan ID {user_id} tidak ditemukan.")
        except Exception as e:
            print(f"Terjadi kesalahan: {e}")
    @staticmethod
    def get_map_link_from_db(self, nama_desa):
        """Fetch the map link from Firebase."""
        try:
            # Fetch the map link from Firebase
            map_link = AdminLogin.db.child("maps").child(nama_desa).get().val()
            return map_link.get('link') if map_link else None  # Assuming 'link' is the key for the URL
        except Exception as e:
            print(f"Error retrieving map link: {e}")
            return None

    @staticmethod
    def update_user_data(user_id, username, nama_lengkap, no_telepon, foto_profil_path=None):
        """Mengupdate data pengguna di database."""
        try:
            user_data = {
                "username": username,
                "namaLengkap": nama_lengkap,
                "noTelepon": no_telepon
            }

            # Update data pengguna
            AdminLogin.db.child("login").child(user_id).update(user_data)

            # Jika ada foto profil yang diupload, upload ke Firebase Storage
            if foto_profil_path:
                storage_path = f"profil_foto/{user_id}.jpg"  # Menggunakan user_id sebagai nama file
                AdminLogin.storage.child(storage_path).put(foto_profil_path)
                user_data['fotoProfil'] = AdminLogin.storage.child(storage_path).get_url(None)
                AdminLogin.db.child("login").child(user_id).update({"fotoProfil": user_data['fotoProfil']})

            print("Data pengguna berhasil diperbarui.")
            return True
        except Exception as e:
            print(f"Error updating user data: {e}")
            return False
class Anggota:
    # Menginisialisasi koneksi ke Firebase
    config = get_firebase_config()
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()

    @staticmethod
    def get_all_anggota():
        """Mengambil semua anggota dari database."""
        try:
            anggota = Anggota.db.child("anggota").get()
            if anggota.each():
                return [(anggota.key(), anggota.val()) for anggota in anggota.each()]
            return []
        except Exception as e:
            print(f"Error getting all anggota: {e}")
            return []
    @staticmethod
    def get_anggota_by_desa(nama_desa):
        """Mengambil semua anggota berdasarkan nama desa."""
        try:
            anggota = Anggota.db.child("anggota").order_by_child("namaDesa").equal_to(nama_desa).get()
            if anggota.each():
                return [(anggota.key(), anggota.val()) for anggota in anggota.each()]
            return []
        except Exception as e:
            print(f"Error getting anggota by desa: {e}")
            return []

    @staticmethod
    def get_anggota(anggota_id):
        """Fetch member data by ID."""
        try:
            anggota_data = Anggota.db.child("anggota").child(anggota_id).get()
            return anggota_data.val()  # Return member data
        except Exception as e:
            print(f"Error getting anggota with ID {anggota_id}: {e}")
            return None

    @staticmethod
    def add_anggota(anggota_data):
        """Menambahkan anggota baru ke database."""
        try:
            print(f"Menambahkan anggota: {anggota_data}")  # Debugging
            return Anggota.db.child("anggota").push(anggota_data)
        except Exception as e:
            print(f"Kesalahan saat menambahkan anggota: {e}")
            raise e

    @staticmethod
    def update_anggota(anggota_id, anggota_data):
        """Memperbarui data anggota berdasarkan ID."""
        try:
            return Anggota.db.child("anggota").child(anggota_id).update(anggota_data)
        except Exception as e:
            print(f"Error updating anggota: {e}")
            raise e

    @staticmethod
    def delete_anggota(anggota_id):
        """Menghapus anggota berdasarkan ID."""
        try:
            return Anggota.db.child("anggota").child(anggota_id).remove()
        except Exception as e:
            print(f"Error deleting anggota: {e}")
            raise e

class Penggunaan:
    @staticmethod
    def get_kemajuan_data_by_title(judul):
        """Mengambil data kemajuan berdasarkan judul."""
        return Penggunaan.get_penggunaan_data_by_title(judul)

    @classmethod
    def update_kemajuan_data_by_title(cls, old_title, new_title, description, date, jumlah, persentase, gambar):
        """Update data kemajuan berdasarkan judul."""
        usage_data = cls.get_kemajuan_data_by_title(old_title)
        if usage_data:
            usage_id = usage_data['id']  # Pastikan Anda memiliki ID yang tepat
            AdminLogin.db.child("penggunaan").child(usage_id).update({
                'judul': new_title,
                'deskripsiKemajuan': description,
                'jumlah': jumlah,
                'tanggal': date,
                'persentase': persentase,
                'gambar': gambar
            })
            print(f"Data kemajuan berhasil diperbarui dari '{old_title}' ke '{new_title}'")

    # @staticmethod
    # def update_image_path_by_title(title, image_path):
    #     """Memperbarui path gambar di database berdasarkan judul."""
    #     try:
    #         AdminLogin.db.child("penggunaan").child(title).update({"gambar": image_path})
    #         print(f"Path gambar berhasil diperbarui untuk judul: {title}")
    #     except Exception as e:
    #         print(f"Error saat memperbarui path gambar: {e}")

    @staticmethod
    def get_penggunaan_data(nama_desa):
        """Mengambil data penggunaan berdasarkan nama desa."""
        try:
            print(f"Mencoba mengambil data untuk nama desa: {nama_desa}")  # Debugging output
            penggunaan_data = AdminLogin.db.child("penggunaan").order_by_child("namaDesa").equal_to(nama_desa).get()
            print(f"Data yang diambil dari database: {penggunaan_data.val()}")  # Debugging output
            
            if penggunaan_data.each():  # Memeriksa apakah ada data
                return [data.val() for data in penggunaan_data.each()]  # Mengembalikan daftar data penggunaan
            
            print("Tidak ada data ditemukan untuk nama desa tersebut.")  # Tambahkan log ini
            return []  # Jika tidak ada data
        except Exception as e:
            print(f"Error getting penggunaan data: {e}")  # Log error
            return []

    @staticmethod
    def add_penggunaan_data(nama_desa, judul, deskripsi, tanggal, jumlah):
        """Menambahkan data penggunaan baru tanpa menyimpan total penggunaan dana."""
        try:
            # Memastikan semua parameter tidak kosong
            if not all([nama_desa, judul, deskripsi, tanggal, jumlah]):
                print("Semua parameter harus diisi.")
                return

            # Menambahkan data penggunaan baru
            AdminLogin.db.child("penggunaan").push({
                "namaDesa": nama_desa,
                "judul": judul,
                "deskripsi": deskripsi,
                "tanggal": tanggal,
                "jumlah": jumlah  # Ganti 'jumlah' dengan kunci yang sesuai
            })

            print("Data penggunaan berhasil ditambahkan.")
        except Exception as e:
            print(f"Error adding penggunaan data: {e}")

    @ staticmethod
    def get_penggunaan_data_by_title(judul):
        """Mengambil data penggunaan berdasarkan judul."""
        try:
            penggunaan_data = AdminLogin.db.child("penggunaan").order_by_child("judul").equal_to(judul).get()
            if penggunaan_data.each():
                # Mengembalikan data dan ID dari entri pertama
                return {**penggunaan_data.each()[0].val(), 'id': penggunaan_data.each()[0].key()}  
            return {}  # Jika tidak ada data
        except Exception as e:
            print(f"Error getting penggunaan data by title: {e}")
            return {}

    @classmethod
    def update_penggunaan_data_by_title(cls, old_title, new_title, description, date, jumlah):
        """Update data penggunaan berdasarkan judul."""
        usage_data = cls.get_penggunaan_data_by_title(old_title)
        if usage_data:
            # Ambil ID dari data yang ada
            usage_id = usage_data['id']  # Pastikan Anda memiliki ID yang tepat
            # Update data di Firebase
            AdminLogin.db.child("penggunaan").child(usage_id).update({
                'judul': new_title,
                'deskripsi': description,
                'jumlah': jumlah,
                'tanggal': date
            })
            print(f"Updated usage data for title: {old_title} to {new_title}")

    @classmethod
    def delete_penggunaan_by_title(cls, title):
        """Delete data penggunaan berdasarkan judul."""
        usage_data = cls.get_penggunaan_data_by_title(title)
        if usage_data:
            # Ambil ID dari data yang ada
            usage_id = usage_data['id']  # Pastikan Anda memiliki ID yang tepat
            # Hapus data dari database
            AdminLogin.db.child("penggunaan").child(usage_id).remove()
            print(f"Deleted usage data for title: {title}")
        else:
            print(f"Data tidak ditemukan untuk judul: {title}")
    
    @staticmethod
    def save_keuangan_data(nama_desa, tambahan_keuangan):
        """Simpan data keuangan desa ke Firebase."""
        try:
            # Ambil data keuangan yang ada
            current_data = AdminLogin.db.child("keuangan").child(nama_desa).get()
            
            if current_data.val():
                # Jika data sudah ada, tambahkan ke total
                total_keuangan = current_data.val().get('total_keuangan', 0) + tambahan_keuangan
            else:
                # Jika tidak ada data, set total keuangan sama dengan tambahan
                total_keuangan = tambahan_keuangan
            
            # Simpan data ke Firebase
            AdminLogin.db.child("keuangan").child(nama_desa).set({
                "total_keuangan": total_keuangan
            })
            print("Data keuangan berhasil disimpan.")
        except Exception as e:
            print(f"Error saat menyimpan data keuangan: {e}")

    @staticmethod
    def get_keuangan_data(nama_desa):
        """Mengambil data keuangan desa dari Firebase."""
        try:
            keuangan_data = AdminLogin.db.child("keuangan").child(nama_desa).get()
            if keuangan_data.val():
                return keuangan_data.val()
            return {}  # Jika tidak ada data
        except Exception as e:
            print(f"Error saat mengambil data keuangan: {e}")
            return {}
    @classmethod
    def update_image_path_by_title(cls, title, image_path):
        """Update the image path for a specific title."""
        try:
            usage_data = cls.get_penggunaan_data_by_title(title)
            if usage_data:
                usage_id = usage_data['id']  # Get the ID of the existing entry
                # Update the image path in Firebase
                AdminLogin.db.child("penggunaan").child(usage_id).update({
                    'gambar': image_path  # Assuming 'gambar' is the key for the image path
                })
                print(f"Updated image path for title: {title}")
            else:
                print(f"No usage data found for title: {title}")
        except Exception as e:
            print(f"Error updating image path: {e}")
