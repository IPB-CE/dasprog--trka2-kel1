from flask import Flask, render_template, request, url_for, flash #Modul Flask untuk membuat web app 
from werkzeug.utils import redirect #Modul untuk mengarahkan ke halaman lain 
from flask_mysqldb import MySQL #Modul untuk menghubungkan ke database MySQL 

app = Flask(__name__) #Membuat objek Flask
app.secret_key = 'random' #Kunci rahasia untuk flash message

app.config['MYSQL_HOST'] = 'localhost' # konfigurasi host database
app.config['MYSQL_USER'] = 'root' #Konfigurasi username database
app.config['MYSQL_PASSWORD'] = 'Naufalrf21' #Konfigurasi password database
app.config['MYSQL_DB'] = 'programnopol' #Konfigurasi database yang digunakan

mysql = MySQL(app) #Membuat objek MySQL dengan parameter app

@app.route('/') #Membuat route untuk halaman index
def Index(): #Membuat fungsi untuk halaman indexz 
    cur = mysql.connection.cursor() #Membuat objek cursor untuk mengeksekusi query
    cur.execute("SELECT * FROM programnopol") #Mengeksekusi query untuk menampilkan data
    data = cur.fetchall() #Menyimpan hasil query ke dalam variabel data
    cur.close() #Menutup objek cursor 

    return render_template('index.html', programnopol=data) #Mengembalikan nilai render_template dengan parameter nama template dan data

@app.route('/insert', methods = ['POST']) #Membuat route untuk insert data
def insert(): #Membuat fungsi untuk insert data
    if request.method == "POST": #Jika request method POST maka jalankan perintah dibawah
        flash("Data Berhasil Ditambahkan") #Menampilkan flash message dengan isi Data Berhasil Ditambahkan
        nama = request.form['nama'] #Menyimpan data dari form nama ke dalam variabel nama 
        plat = request.form['plat'] #Menyimpan data dari form plat ke dalam variabel plat
        cur = mysql.connection.cursor() #Membuat objek cursor untuk mengeksekusi query
        cur.execute("INSERT INTO programnopol (nama, plat) VALUES (%s, %s)", (nama, plat)) #Mengeksekusi query untuk insert data
        mysql.connection.commit() #Menyimpan perubahan data
        return redirect(url_for('Index')) #Mengembalikan nilai redirect dengan parameter url_for Index untuk mengarahkan ke halaman index

@app.route('/delete/<string:no_data>', methods = ['GET']) #Membuat route untuk delete data
def delete(no_data): #Membuat fungsi untuk delete data 
    flash("Data Berhasil Dihapus") #Menampilkan flash message dengan isi Data Berhasil Dihapus
    cur = mysql.connection.cursor() #Membuat objek cursor untuk mengeksekusi query
    cur.execute("DELETE FROM programnopol WHERE no=%s", (no_data,)) #Mengeksekusi query untuk delete data 
    mysql.connection.commit() #Menyimpan perubahan data 
    return redirect(url_for('Index')) #Mengembalikan nilai redirect dengan parameter url_for Index untuk mengarahkan ke halaman index

@app.route('/update', methods= ['POST', 'GET']) #Membuat route untuk update data 
def update(): #Membuat fungsi untuk update data 
    if request.method == 'POST': #Jika request method POST maka jalankan perintah dibawah 
        no_data = request.form['no'] #Menyimpan data dari form no ke dalam variabel no_data 
        nama = request.form['nama'] #Menyimpan data dari form nama ke dalam variabel nama 
        plat = request.form['plat'] #Menyimpan data dari form plat ke dalam variabel plat 
        cur = mysql.connection.cursor() #Membuat objek cursor untuk mengeksekusi query
        cur.execute("""
        UPDATE programnopol SET nama=%s, plat=%s 
        WHERE no=%s 
        """, (nama, plat, no_data)) #Mengeksekusi query untuk update data 
        flash("Data Updated Successfully") #Menampilkan flash message dengan isi Data Updated Successfully
        return redirect(url_for('Index')) #Mengembalikan nilai redirect dengan parameter url_for Index untuk mengarahkan ke halaman index

if __name__ == "__main__":  #Jika file ini dijalankan maka jalankan perintah dibawah 
    app.run(debug=True)  #Menjalankan web app dengan mode debug