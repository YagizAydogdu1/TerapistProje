import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QTableWidget, QTableWidgetItem, QTabWidget, 
                             QMessageBox, QTextEdit, QHeaderView, QDateTimeEdit, QStackedWidget)
from PyQt5.QtCore import Qt, QDateTime
from database import Veritabani

class TerapistSistemi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.vt = Veritabani()
        self.setWindowTitle("Terapist ve Danışan Yönetim Sistemi")
        self.resize(1100, 750)

        self.sayfalar = QStackedWidget()
        self.setCentralWidget(self.sayfalar)

        self.sayfa_giris_secim()
        self.sayfa_terapist_login()
        self.sayfa_danisan_login()

    def sayfa_giris_secim(self):
        self.widget_secim = QWidget()
        layout = QVBoxLayout(self.widget_secim)
        layout.setAlignment(Qt.AlignCenter)
        baslik = QLabel("<h1>Hoş Geldiniz</h1><p>Lütfen giriş tipini seçiniz</p>")
        baslik.setAlignment(Qt.AlignCenter)
        btn_terapist = QPushButton(" TERAPİST GİRİŞİ")
        btn_danisan = QPushButton(" DANIŞAN GİRİŞİ")
        
        stil_t = "QPushButton { font-size: 18px; padding: 20px; border-radius: 10px; background-color: #2c3e50; color: white; margin: 10px; }"
        stil_d = "QPushButton { font-size: 18px; padding: 20px; border-radius: 10px; background-color: #27ae60; color: white; margin: 10px; }"
        btn_terapist.setStyleSheet(stil_t); btn_danisan.setStyleSheet(stil_d)

        btn_terapist.clicked.connect(lambda: self.sayfalar.setCurrentIndex(1))
        btn_danisan.clicked.connect(lambda: self.sayfalar.setCurrentIndex(2))

        layout.addStretch(); layout.addWidget(baslik)
        layout.addWidget(btn_terapist); layout.addWidget(btn_danisan); layout.addStretch()
        self.sayfalar.addWidget(self.widget_secim)

    def sayfa_terapist_login(self):
        widget = QWidget(); layout = QVBoxLayout(widget); layout.setAlignment(Qt.AlignCenter)
        self.t_kullanici = QLineEdit(); self.t_kullanici.setPlaceholderText("Kullanıcı Adı")
        self.t_sifre = QLineEdit(); self.t_sifre.setPlaceholderText("Şifre"); self.t_sifre.setEchoMode(QLineEdit.Password)
        btn_giris = QPushButton("Sisteme Gir"); btn_giris.clicked.connect(self.kontrol_terapist)
        btn_geri = QPushButton("Ana Ekrana Dön"); btn_geri.clicked.connect(lambda: self.sayfalar.setCurrentIndex(0))
        layout.addWidget(QLabel("<h2>Terapist Girişi</h2>"))
        layout.addWidget(self.t_kullanici); layout.addWidget(self.t_sifre)
        layout.addWidget(btn_giris); layout.addWidget(btn_geri)
        self.sayfalar.addWidget(widget)

    def sayfa_danisan_login(self):
        widget = QWidget(); layout = QVBoxLayout(widget); layout.setAlignment(Qt.AlignCenter)
        self.d_ad = QLineEdit(); self.d_ad.setPlaceholderText("Ad Soyadınız")
        self.d_tel = QLineEdit(); self.d_tel.setPlaceholderText("Telefon Numaranız")
        btn_sorgula = QPushButton("Randevumu Bul"); btn_sorgula.clicked.connect(self.kontrol_danisan)
        btn_geri = QPushButton("Ana Ekrana Dön"); btn_geri.clicked.connect(lambda: self.sayfalar.setCurrentIndex(0))
        layout.addWidget(QLabel("<h2>Danışan Sorgulama</h2>"))
        layout.addWidget(self.d_ad); layout.addWidget(self.d_tel)
        layout.addWidget(btn_sorgula); layout.addWidget(btn_geri)
        self.sayfalar.addWidget(widget)

    def kontrol_terapist(self):
        if self.t_kullanici.text() == self.vt.t_user and self.t_sifre.text() == self.vt.t_pass:
            self.panel_terapist_ac()
        else: QMessageBox.warning(self, "Hata", "Bilgiler yanlış!")

    def kontrol_danisan(self):
        sonuc = self.vt.danisan_ara(self.d_ad.text(), self.d_tel.text())
        if sonuc: self.panel_danisan_ac(sonuc)
        else: QMessageBox.critical(self, "Hata", "Randevu bulunamadı!")

    def panel_terapist_ac(self):
        self.t_paneli = QWidget(); layout = QVBoxLayout(self.t_paneli)
        self.sekme_grubu = QTabWidget()
        
        ekle_w = QWidget(); e_lay = QVBoxLayout()
        self.in_ad = QLineEdit(); self.in_ad.setPlaceholderText("Ad Soyad...")
        self.in_tel = QLineEdit(); self.in_tel.setPlaceholderText("Telefon...")
        self.in_mail = QLineEdit(); self.in_mail.setPlaceholderText("E-posta adresi...")
        self.in_not = QTextEdit(); self.in_not.setPlaceholderText("Notlar...")
        self.in_date = QDateTimeEdit(QDateTime.currentDateTime()); self.in_date.setCalendarPopup(True)
        
        btn_kayit = QPushButton("DANIŞANI VE RANDEVUYU KAYDET")
        btn_kayit.setStyleSheet("background-color: #2c3e50; color: white; padding: 10px;")
        btn_kayit.clicked.connect(self.kaydet_islem)
        
        e_lay.addWidget(QLabel("Danışan Adı:")); e_lay.addWidget(self.in_ad)
        e_lay.addWidget(QLabel("Telefon:")); e_lay.addWidget(self.in_tel)
        e_lay.addWidget(QLabel("E-posta:")); e_lay.addWidget(self.in_mail)
        e_lay.addWidget(QLabel("Randevu Tarihi:")); e_lay.addWidget(self.in_date)
        e_lay.addWidget(QLabel("Notlar:")); e_lay.addWidget(self.in_not)
        e_lay.addWidget(btn_kayit); e_lay.addStretch()
        ekle_w.setLayout(e_lay); self.sekme_grubu.addTab(ekle_w, " Randevu Ekle")

        liste_w = QWidget(); l_lay = QVBoxLayout()
        self.tablo = QTableWidget(); self.tablo.setColumnCount(6)
        self.tablo.setHorizontalHeaderLabels(["İsim", "Tel", "Randevu", "E-posta", "Kayıt", "ID"])
        self.tablo.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tablo.setColumnHidden(5, True)
        btn_sil = QPushButton(" Seçili Kaydı Sil"); btn_sil.setStyleSheet("background-color: #c0392b; color: white;")
        btn_sil.clicked.connect(self.sil_islem)
        l_lay.addWidget(btn_sil); l_lay.addWidget(self.tablo)
        liste_w.setLayout(l_lay); self.sekme_grubu.addTab(liste_w, " Randevu Listesi")

        layout.addWidget(self.sekme_grubu)
        self.tabloyu_guncelle()
        self.sayfalar.addWidget(self.t_paneli); self.sayfalar.setCurrentWidget(self.t_paneli)

    def panel_danisan_ac(self, veri):
        d_paneli = QWidget(); layout = QVBoxLayout(d_paneli)
        layout.addWidget(QLabel(f"<h2>Hoş Geldiniz, {veri['ad_soyad']}</h2>"))
        bilgi = QTextEdit(); bilgi.setReadOnly(True)
        bilgi.setText(f"Randevu Tarihiniz: {veri['randevu_tarihi']}\n\nE-posta: {veri.get('email', 'Girilmemiş')}\n\nNotlar: {veri['notlar']}")
        layout.addWidget(bilgi)
        btn_cikis = QPushButton("Çıkış Yap"); btn_cikis.clicked.connect(lambda: sys.exit())
        layout.addWidget(btn_cikis)
        self.sayfalar.addWidget(d_paneli); self.sayfalar.setCurrentWidget(d_paneli)

    def kaydet_islem(self):
        if self.in_ad.text() and self.in_tel.text():
            self.vt.kaydet(self.in_ad.text(), self.in_tel.text(), self.in_mail.text(), 
                           self.in_not.toPlainText(), self.in_date.dateTime().toString("dd-MM-yyyy HH:mm"))
            QMessageBox.information(self, "Başarılı", "Kayıt tamamlandı.")
            self.in_ad.clear(); self.in_tel.clear(); self.in_mail.clear(); self.in_not.clear()
            self.tabloyu_guncelle()
        else: QMessageBox.warning(self, "Hata", "Ad ve Telefon zorunludur!")

    def sil_islem(self):
        row = self.tablo.currentRow()
        if row > -1:
            if QMessageBox.question(self, "Onay", "Silmek istiyor musunuz?") == QMessageBox.Yes:
                self.vt.sil(self.tablo.item(row, 5).text()); self.tabloyu_guncelle()
        else: QMessageBox.warning(self, "Hata", "Bir satır seçin!")

    def tabloyu_guncelle(self):
        veriler = self.vt.listele(); self.tablo.setRowCount(0)
        for i, v in enumerate(veriler):
            self.tablo.insertRow(i)
            self.tablo.setItem(i, 0, QTableWidgetItem(v.get('ad_soyad', "")))
            self.tablo.setItem(i, 1, QTableWidgetItem(v.get('telefon', "")))
            self.tablo.setItem(i, 2, QTableWidgetItem(v.get('randevu_tarihi', "")))
            self.tablo.setItem(i, 3, QTableWidgetItem(v.get('email', "")))
            self.tablo.setItem(i, 4, QTableWidgetItem(v.get('kayit_tarihi', "")))
            self.tablo.setItem(i, 5, QTableWidgetItem(str(v['_id'])))