from datetime import datetime
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="skripsi-3"
)

cursor = db.cursor()

kemarin = datetime.now().date()

def cek_waktu(waktu):
    global kemarin  # Mengakses variabel global 'kemarin'
    today = datetime.now().date()
    if today != kemarin:
        #disini bisa ditambah kode untuk export absen kemarin
        kemarin = today
        return False
    else:
        return True

def absen(name):
    cek = cek_waktu(kemarin) 
    if cek:
        cursor.execute("SELECT * FROM absen")
        results = cursor.fetchall()
        if results == []:
            results.append("push")
        for result in results:
            if result[0] == name:
                print("Nama tersebut sudah absen")
            else:
                waktu = datetime.now()
                sql = "INSERT INTO absen (name, waktu_absen) VALUES (%s, %s)"
                val = (name, waktu)
                cursor.execute(sql, val)
                print("absen berhasil")
    else:
        print("kemarin")
        cursor.execute("DELETE FROM absen")
        absen(name)
    db.commit()
