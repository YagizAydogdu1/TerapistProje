from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

class Veritabani:
    def __init__(self):
        try:
            self.client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=2000)
            self.db = self.client['terapist_v3_db']
            self.danisanlar = self.db['danisanlar']
            self.t_user, self.t_pass = "admin", "1234"
        except Exception as e:
            print(f"VERİTABANI HATASI: {e}")

    def kaydet(self, ad, tel, mail, notlar, randevu):
        veri = {
            "ad_soyad": ad, "telefon": tel, "email": mail, "notlar": notlar, 
            "randevu_tarihi": randevu, 
            "kayit_tarihi": datetime.now().strftime("%d-%m-%Y %H:%M")
        }
        return self.danisanlar.insert_one(veri)

    def listele(self):
        return list(self.danisanlar.find().sort("randevu_tarihi", 1))

    def sil(self, id_str):
        return self.danisanlar.delete_one({"_id": ObjectId(id_str)})

    def danisan_ara(self, ad, tel):
        return self.danisanlar.find_one({"ad_soyad": ad, "telefon": tel})