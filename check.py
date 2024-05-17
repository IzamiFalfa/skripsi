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
                waktu = datetime.now()
                sql = "UPDATE absen SET absen = %s, waktu_absen = %s WHERE name = %s"
                val = ("Sudah", waktu, name)
                cursor.execute(sql, val)
                print("absen berhasil")
    else:
        print("kemarin")
        sql = "UPDATE absen SET absen = %s, waktu_absen = %s"
        val = ("Belum", "NULL")
        cursor.execute(sql, val)
        absen(name)
    db.commit()

