from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import re
# initial app web
web = Flask(__name__)
web.secret_key = '2v2Yp7XSS9cC5WcbGk3l7PijY5bW4zwJ'

db = mysql.connector.connect(
  host="localhost",
  port="3306",
  user="root",
  passwd="",
  database="kelas_c"
)
# # # initial mysql database
# mysql = MySQL()
# web.config['MYSQL_DATABASE_HOST'] = 'localhost'
# web.config['MYSQL_DATABASE_PORT'] = 8889
# web.config['MYSQL_DATABASE_USER'] = 'root'
# web.config['MYSQL_DATABASE_PASSWORD'] = ''
# web.config['MYSQL_DATABASE_DB'] = 'kelas_c'
# mysql.init_app(web)


@web.route('/')
def Home():
    return render_template('home.html')

@web.route('/login', methods=(['GET', 'POST']))
def Login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM tb_users WHERE username='{username}' AND password='{password}'")
        user = cursor.fetchone()
        if user:
            session['loggedin'] =True
            session['id'] = user[0]
            session['username'] = user[0]
            msg="Login Berhasil"
            return render_template('home.html', msg=msg)
        else:
            msg = 'Periksa Username atau password'            
    return render_template('login.html', msg=msg)

@web.route('/register', methods=(['GET', 'POST']))
def Register():
    msg = ''
    if request.method == "POST" and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM tb_users WHERE username='{username}'")
        user = cursor.fetchone()
        if user:
            msg = 'Akun sudah ada'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'email tidak valid'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'username harus karakter, number'
        elif not username or not password or not email:
            msg = 'silahkan isi form'
        else:
            cursor.execute(f"INSERT INTO tb_users VALUES (NULL, '{username}', '{password}', '{email}')")
            db.commit()
            msg = 'Register berhasil'
            return redirect('/login')
    elif request.method == "POST":
        msg = 'silahkan isi form'
    return render_template('register.html', msg=msg)

@web.route('/logout')
def Logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect('/login')

@web.route('/mahasiswa')
def ListMahasiswa():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tb_mahasiswa")
    result = cursor.fetchall()

    return render_template('list_mhs.html', data=result)

@web.route('/form', methods=['GET', 'POST'])
def Form():
    if request.method == 'POST':
        data = request.form
        nama = data['nama']
        nim = data['nim']
        alamat = data['alamat']

        cursor = db.cursor()
        query = f"INSERT INTO tb_mahasiswa (nama, nim, alamat) VALUES('{nama}', '{nim}', '{alamat}')"
        cursor.execute(query)
        db.commit()

        return redirect('/mahasiswa', code=302, Response=None)
    
    return render_template('form.html')


@web.route('/hapus/<id>')
def HapusMhs(id):
    cursor = db.cursor()
    query = f"DELETE FROM tb_mahasiswa WHERE id='{id}'"
    cursor.execute(query)
    db.commit()

    return redirect('/mahasiswa', code=302, Response=None)

@web.route("/edit/<id>", methods=["GET", "POST"])
def edit(id):
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM tb_mahasiswa WHERE id='{id}'")
    data = cursor.fetchone()
    if request.method == "POST":
        id = request.form['id']
        nama = request.form['nama']
        nim = request.form['nim']
        alamat = request.form['alamat']
        sql = (f"UPDATE tb_mahasiswa SET nama='{nama}', nim='{nim}', alamat='{alamat}' WHERE id='{id}'")
        # val = (nama, nim, alamat, id)
        cursor.execute(sql)
        db.commit()
        return redirect('/mahasiswa')
    else:
        return render_template('edit.html', data=data, code=302, Response=None)

# @web.route('/login', methods=['GET', 'POST'])
# def login():
#     msg = ''
#     return render_template('login.html', msg='')






if __name__ == '__main__':
    web.run()