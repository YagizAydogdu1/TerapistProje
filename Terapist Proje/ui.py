import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QTableWidget, 
                             QTableWidgetItem, QTabWidget, QMessageBox, 
                             QTextEdit, QHeaderView, QDateTimeEdit, QStackedWidget)
from PyQt5.QtCore import Qt, QDateTime
from database import Veritabani 

class TerapistSistemi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.vt = Veritabani()
        self.setWindowTitle("Terapist & Danışan Yönetim Sistemi")
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
        
        baslik = QLabel("<h1>Hoş Geldiniz</h1><p>Giriş Tipini Seçiniz</p>")
        baslik.setAlignment(Qt.AlignCenter)
        
        btn_terapist = QPushButton(" TERAPİST GİRİŞİ")
        btn_danisan = QPushButton(" DANIŞAN GİRİŞİ")
        
        btn_terapist.setStyleSheet("QPushButton { font-size: 18px; padding: 20px; background-color: #2c3e50; color: white; border-radius: 10px; }")
        btn_danisan.setStyleSheet("QPushButton { font-size: 18px; padding: 20px; background-color: #27ae60; color: white; border-radius: 10px; }")

        btn_terapist.clicked.connect(lambda: self.sayfalar.setCurrentIndex(1))
        btn_danisan.clicked.connect(lambda: self.sayfalar.setCurrentIndex(2))

        layout.addStretch(); layout.addWidget(baslik)
        layout.addWidget(btn_terapist); layout.addWidget(btn_danisan); layout.addStretch()
        self.sayfalar.addWidget(self.widget_secim)

    def sayfa_terapist_login(self):
        widget = QWidget(); layout = QVBoxLayout(widget); layout.setAlignment(Qt.AlignCenter)
        self.t_user = QLineEdit(); self.t_user.setPlaceholderText("Kullanıcı Adı")
        self.t_pass = QLineEdit(); self.t_pass.setPlaceholderText("Şifre"); self.t_pass.setEchoMode(QLineEdit.Password)
        btn = QPushButton("Giriş Yap"); btn.clicked.connect(self.kontrol_terapist)
        btn_g = QPushButton("Geri"); btn_g.clicked.connect(lambda: self.sayfalar.setCurrentIndex(0))
        
        layout.addWidget(QLabel("<h2>Terapist Girişi</h2>"))
        layout.addWidget(self.t_user); layout.addWidget(self.t_pass); layout.addWidget(btn); layout.addWidget(btn_g)
        self.sayfalar.addWidget(widget)

    def sayfa_danisan_login(self):
        widget = QWidget(); layout = QVBoxLayout(widget); layout.setAlignment(Qt.AlignCenter)
        self.d_ad = QLineEdit(); self.d_ad.setPlaceholderText("Ad Soyadınız")
        self.d_tel = QLineEdit(); self.d_tel.setPlaceholderText("Telefon No")
        btn = QPushButton("Randevumu Bul"); btn.clicked.connect(self.kontrol_danisan)
        btn_g = QPushButton("Geri"); btn_g.clicked.connect(lambda: self.sayfalar.setCurrentIndex(0))
        
        layout.addWidget(QLabel("<h2>Danışan Girişi</h2>"))
        layout.addWidget(self.d_ad); layout.addWidget(self.d_tel); layout.addWidget(btn); layout.addWidget(btn_g)
        self.sayfalar.addWidget(widget)

    def kontrol_terapist(self):
        if self.t_user.text() == self.vt.t_user and self.t_pass.text() == self.vt.t_pass:
            self.panel_terapist_ac()
        else: QMessageBox.warning(self, "Hata", "Bilgiler yanlış!")

    def kontrol_danisan(self):
        sonuc = self.vt.danisan_ara(self.d_ad.text(), self.d_tel.text())
        if sonuc: self.panel_danisan_ac(sonuc)
        else: QMessageBox.critical(self, "Hata", "Randevu bulunamadı!")

    def panel_terapist_ac(self):
        self.t_paneli = QWidget(); layout = QVBoxLayout(self.t_paneli)
        self.sekme_grubu = QTabWidget()
        
        #Randevu Ekleme Sekmesi
        ekle_w = QWidget(); e_lay = QVBoxLayout()
        self.in_ad = QLineEdit(); self.in_tel = QLineEdit(); self.in_mail = QLineEdit()
        self.in_not = QTextEdit(); self.in_date = QDateTimeEdit(QDateTime.currentDateTime())
        self.in_date.setCalendarPopup(True)
        btn_k = QPushButton("KAYDET"); btn_k.clicked.connect(self.kaydet_islem)
        
        e_lay.addWidget(QLabel("Ad Soyad:")); e_lay.addWidget(self.in_ad)
        e_lay.addWidget(QLabel("Telefon:")); e_lay.addWidget(self.in_tel)
        e_lay.addWidget(QLabel("E-posta:")); e_lay.addWidget(self.in_mail)
        e_lay.addWidget(QLabel("Tarih:")); e_lay.addWidget(self.in_date)
        e_lay.addWidget(QLabel("Notlar:")); e_lay.addWidget(self.in_not)
        e_lay.addWidget(btn_k); e_lay.addStretch()
        ekle_w.setLayout(e_lay); self.sekme_grubu.addTab(ekle_w, " Yeni Kayıt")

        #Liste Sekmesi
        liste_w = QWidget(); l_lay = QVBoxLayout()
        self.tablo = QTableWidget(); self.tablo.setColumnCount(6)
        self.tablo.setHorizontalHeaderLabels(["İsim", "Tel", "Randevu", "E-posta", "Kayıt", "ID"])
        self.tablo.setColumnHidden(5, True)
        self.tablo.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        btn_s = QPushButton(" Seçiliyi Sil"); btn_s.clicked.connect(self.sil_islem)
        l_lay.addWidget(btn_s); l_lay.addWidget(self.tablo)
        liste_w.setLayout(l_lay); self.sekme_grubu.addTab(liste_w, " Liste")

        layout.addWidget(self.sekme_grubu)
        self.tabloyu_guncelle()
        self.sayfalar.addWidget(self.t_paneli); self.sayfalar.setCurrentWidget(self.t_paneli)

    def panel_danisan_ac(self, veri):
        d_paneli = QWidget(); layout = QVBoxLayout(d_paneli)
        layout.addWidget(QLabel(f"<h2>Hoş Geldiniz, {veri['ad_soyad']}</h2>"))
        bilgi = QTextEdit(); bilgi.setReadOnly(True)
        bilgi.setText(f"Randevu: {veri['randevu_tarihi']}\n\nNotlar: {veri['notlar']}")
        layout.addWidget(bilgi)
        btn = QPushButton("Çıkış"); btn.clicked.connect(lambda: sys.exit())
        layout.addWidget(btn)
        self.sayfalar.addWidget(d_paneli); self.sayfalar.setCurrentWidget(d_paneli)

    def kaydet_islem(self):
        self.vt.kaydet(self.in_ad.text(), self.in_tel.text(), self.in_mail.text(), 
                       self.in_not.toPlainText(), self.in_date.dateTime().toString("dd-MM-yyyy HH:mm"))
        QMessageBox.information(self, "Tamam", "Kaydedildi")
        self.tabloyu_guncelle()

    def sil_islem(self):
        row = self.tablo.currentRow()
        if row > -1:
            self.vt.sil(self.tablo.item(row, 5).text()); self.tabloyu_guncelle()

    def tabloyu_guncelle(self):
        veriler = self.vt.listele(); self.tablo.setRowCount(0)
        for i, v in enumerate(veriler):
            self.tablo.insertRow(i)
            self.tablo.setItem(i, 0, QTableWidgetItem(v['ad_soyad']))
            self.tablo.setItem(i, 1, QTableWidgetItem(v['telefon']))
            self.tablo.setItem(i, 2, QTableWidgetItem(v['randevu_tarihi']))
            self.tablo.setItem(i, 3, QTableWidgetItem(v.get('email', '')))
            self.tablo.setItem(i, 4, QTableWidgetItem(v['kayit_tarihi']))
            self.tablo.setItem(i, 5, QTableWidgetItem(str(v['_id'])))