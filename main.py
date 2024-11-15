from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.properties import StringProperty
import webbrowser

# Import semua layar yang diperlukan
from splash import SplashScreen
from user_access.beranda import BerandaScreen
from user_access.penggunaan import PenggunaanScreen
from user_access.kemajuan import KemajuanScreen
from user_access.profil import ProfileScreen
from login.login import LoginScreen
from login.buat_akun import BuatAkunScreen
from login.tautkan_akun import TautkanAkunScreen
from admin.adm_beranda import AdmBerandaScreen
from admin.adm_penggunaan import AdmPenggunaanScreen
from admin.adm_kemajuan import AdmKemajuanScreen
from admin.adm_profil import AdmProfileScreen
from access.anggota import AnggotaScreen
from access.anggotatb import TambahAnggotaScreen
from access.penggunaan_edit import PenggunaanEditScreen
from access.penggunaan_tambah import PenggunaanTambahScreen
from access.kemajuan_edit import KemajuanEditScreen
from access.biodata import BiodataScreen
from access.ubah_sandi import UbahSandiScreen
from access.pengaturan_akun import PengaturanAkunScreen
from access.dana_desa import DanaDesaScreen
from pengguna.peng_beranda import PengBerandaScreen
from pengguna.peng_penggunaan import PengPenggunaanScreen
from pengguna.peng_kemajuan import PengKemajuanScreen
from pengguna.peng_profil import PengProfileScreen
from access.user_anggota import UserAnggotaScreen
from access.user_penggunaan import UserPenggunaanScreen
from access.user_kemajuan import UserKemajuanScreen
from access.user_biodata import UserBiodataScreen
from access.user_ubah_sandi import UserUbahSandiScreen
from access.user_pengaturan_akun import UserPengaturanAkunScreen
from access.user_dana_desa import UserDanaDesaScreen


# Atur ukuran jendela secara eksplisit
Window.size = (350, 600)
# Window.fullscreen = True

# Muat file KV yang sesuai dengan layar
Builder.load_file('user_access/beranda.kv')             
Builder.load_file('user_access/penggunaan.kv')  
Builder.load_file('user_access/kemajuan.kv') 
Builder.load_file('user_access/profil.kv') 
Builder.load_file('login/login.kv')         
Builder.load_file('login/buat_akun.kv')     
Builder.load_file('login/tautkan_akun.kv')  
Builder.load_file('admin/adm_beranda.kv')             
Builder.load_file('admin/adm_penggunaan.kv')  
Builder.load_file('admin/adm_kemajuan.kv') 
Builder.load_file('admin/adm_profil.kv') 
Builder.load_file('access/anggota.kv')
Builder.load_file('access/anggotatb.kv')
Builder.load_file('access/penggunaan_edit.kv')
Builder.load_file('access/penggunaan_tambah.kv')
Builder.load_file('access/kemajuan_edit.kv')
Builder.load_file('access/biodata.kv')
Builder.load_file('access/ubah_sandi.kv')
Builder.load_file('access/pengaturan_akun.kv')
Builder.load_file('access/dana_desa.kv')
Builder.load_file('pengguna/peng_beranda.kv')
Builder.load_file('pengguna/peng_penggunaan.kv')
Builder.load_file('pengguna/peng_kemajuan.kv')
Builder.load_file('pengguna/peng_profil.kv')
Builder.load_file('access/user_anggota.kv')
Builder.load_file('access/user_penggunaan.kv')
Builder.load_file('access/user_kemajuan.kv')
Builder.load_file('access/user_biodata.kv')
Builder.load_file('access/user_ubah_sandi.kv')
Builder.load_file('access/user_pengaturan_akun.kv')
Builder.load_file('access/user_dana_desa.kv')
Builder.load_file('splash.kv')
   
class MyScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(SplashScreen(name='splash'))  # Tambahkan splash screen
        self.add_widget(BerandaScreen(name='beranda'))
        self.add_widget(PenggunaanScreen(name='penggunaan'))
        self.add_widget(KemajuanScreen(name='kemajuan'))
        self.add_widget(ProfileScreen(name='profil'))
        self.add_widget(LoginScreen(name='login'))
        self.add_widget(BuatAkunScreen(name='buat_akun'))
        self.add_widget(TautkanAkunScreen(name='tautkan_akun'))
        self.add_widget(AdmBerandaScreen(name='adm_beranda'))
        self.add_widget(AdmPenggunaanScreen(name='adm_penggunaan'))
        self.add_widget(AdmKemajuanScreen(name='adm_kemajuan'))
        self.add_widget(AdmProfileScreen(name='adm_profil'))
        self.add_widget(AnggotaScreen(name='anggota'))
        self.add_widget(TambahAnggotaScreen(name='anggotatb'))
        self.add_widget(PenggunaanEditScreen(name='penggunaan_edit'))
        self.add_widget(PenggunaanTambahScreen(name='penggunaan_tambah'))
        self.add_widget(KemajuanEditScreen(name='kemajuan_edit'))
        self.add_widget(BiodataScreen(name='biodata'))
        self.add_widget(UbahSandiScreen(name='ubah_sandi'))
        self.add_widget(PengaturanAkunScreen(name='pengaturan_akun'))
        self.add_widget(DanaDesaScreen(name='dana_desa'))
        self.add_widget(PengBerandaScreen(name='peng_beranda'))
        self.add_widget(PengPenggunaanScreen(name='peng_penggunaan'))
        self.add_widget(PengKemajuanScreen(name='peng_kemajuan'))
        self.add_widget(PengProfileScreen(name='peng_profil'))
        self.add_widget(UserAnggotaScreen(name='user_anggota'))
        self.add_widget(UserPenggunaanScreen(name='user_penggunaan'))
        self.add_widget(UserKemajuanScreen(name='user_kemajuan'))
        self.add_widget(UserBiodataScreen(name='user_biodata'))
        self.add_widget(UserUbahSandiScreen(name='user_ubah_sandi'))
        self.add_widget(UserPengaturanAkunScreen(name='user_pengaturan_akun'))
        self.add_widget(UserDanaDesaScreen(name='user_dana_desa'))

class MainApp(MDApp):
    def build(self):
        return MyScreenManager()

if __name__ == '__main__':
    MainApp().run()