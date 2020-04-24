from flask import Flask, session, redirect, url_for, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
import hashlib
app = Flask(__name__)
app.secret_key = "my_name"
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///borang.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# 80abd1c7b39878f896b4d09b68f08217f9e6d5b321db974dd5d24fc762bcb06f

kriteria = [
    'Visi, Misi, Tujuan, dan Sasaran, serta Strategi Pencapaian',
    'Tata Pamong, Kepemimpinan, Sistem Pengelolaan, dan Penjaminan Mutu',
    'Mahasiswa dan Lulusan',
    'Sumber Daya Manusia',
    'Kurikulum, Pembelajaran, dan Suasana Akademik',
    'Pembiayaan, Sarana dan Prasarana, serta Sistem Informasi',
    'Penelitian, Pelayanan/Pengabdian Kepada Masyarakat, dan Kerjasama'
]

daftar_prodi = [
    [
        'S1 Teknik Telekomunikasi',
        'S1 Teknik Telekomunikasi (Internasional)',
        'S1 Teknik Elektro',
        'S1 Teknik Elektro (Internasional)',
        'S1 Teknik Fisika',
        'S1 Teknik Komputer',
        'S2 Teknik Elektro-Telekomunikasi'
    ],
    [
        'S1 Informatika',
        'S1 Informatika (Internasional)',
        'S1 Teknologi Informasi',
        'S1 Rekayasa Perangkat Lunak',
        'S2 Informatika'
    ],
    [
        'S1 Teknik Industri',
        'S1 Teknik Industri (Internasional)',
        'S1 Sistem Informasi',
        'S1 Sistem Informasi (Internasional)',
        'S1 Teknik Logistik',
        'S2 Teknik Industri'
    ],
    [
        'S1 International ICT Business',
        'S1 Manajemen Bisnis Telekomunikasi & Informatika (MBTI)',
        'S1 Akuntansi',
        'S2 Manajemen'
    ],
    [
        'S1 Administrasi Bisnis',
        'S1 Administrasi Bisnis (Internasional)',
        'S1 Ilmu Komunikasi',
        'S1 Ilmu Komunikasi (Internasional)',
        'S1 Digital Public Relation'
    ],
    [
        'S1 Desain Komunikasi Visual',
        'S1 Desain Komunikasi Visual (Internasional)',
        'S1 Product Innovation & Management',
        'S1 Desain Interior',
        'S1 Kriya (Fashion and Textile Design)',
        'S1 Visual Arts (Seni Rupa)',
        'S2 Desain'
    ],
    [
        'D3 Teknologi Telekomunikasi',
        'D3 Teknik Informatika',
        'D3 Sistem Informasi',
        'D3 Sistem Informasi Akuntansi',
        'D3 Teknologi Komputer',
        'D3 Digital Marketing',
        'D3 Perhotelan'
    ]
]

daftar_fakultas = [
    'Fakultas Teknik Elektro',
    'Fakultas Teknik Informatika',
    'Fakultas Rekayasa Industri',
    'Fakultas Ekonomi dan Bisnis',
    'Fakultas Komunikasi dan Bisnis',
    'Fakultas Industri Kreatif',
    'Fakultas Ilmu Terapan'
]

length = len(daftar_fakultas)

presentasi = [
    2.62,
    26.32,
    13.16,
    18.42,
    7.89,
    18.42,
    13.16
]

id_kriteria = [f"krit{x}" for x in range(14)]


def encrypt_string(hash_string):
    sha_signature = hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature


class User(db.Model):
    id_user = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50))
    username = db.Column(db.String(50))
    password = db.Column(db.String(64))
    level = db.Column(db.String(14))
    prodi = db.Column(db.String(30), nullable=True)

    def __init__(self, email, username, password, level, prodi):
        self.email = email
        self.username = username
        self.password = password
        self.level = level
        self.prodi = prodi

    def __str__(self):
        return self.username


class Borang(db.Model):
    id_borang = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isi = db.Column(db.String(14))
    username_kaprodi = db.Column(db.String(50), nullable=True)
    prodinya = db.Column(db.String(30), nullable=True)

    def __init__(self, isi, username_kaprodi, prodinya):
        self.isi = isi
        self.username_kaprodi = username_kaprodi
        self.prodinya = prodinya

    def __str__(self):
        return self.username_kaprodi


class Skor(db.Model):
    id_skor = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prodinya = db.Column(db.String(30), nullable=True)
    skor = db.Column(db.Integer)

    def __init__(self, prodinya, skor):
        self.prodinya = prodinya
        self.skor = skor

    def __str__(self):
        return self.prodinya


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        if "status" in session:
            if session["status"] == "active":
                flash("You are already logged in")
                return redirect(url_for("home"))
            else:
                return render_template("login.html")
        else:
            return render_template("login.html")
    else:
        username = request.form["username"]
        password = encrypt_string(request.form["password"])
        found_user = User.query.filter_by(username=username).first()
        if found_user:
            if found_user.password == password:
                email = found_user.email
                level = found_user.level
                prodi_login = found_user.prodi
                session["username"] = username
                session["email"] = email
                session["level"] = level
                session["status"] = "active"
                session["prodi"] = prodi_login
                flash("Login success")
                return redirect(url_for("home"))
            else:
                flash("Password wrong")
                return redirect(url_for("login"))
        else:
            flash("Username not found")
            return redirect(url_for("login"))


# /akun, /soal, /penilaian, /hasil
@app.route("/")
def home():
    if "status" in session:
        if session["status"] == "active":
            username = session["username"]
            level = session["level"]
            email = session["email"]
            return render_template("home.html", username=username, level=level, email=email)
        else:
            flash("You are not logged in yet")
            return redirect(url_for("login"))
    else:
        session["status"] = "inactive"
        flash("You are not logged in yet")
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.pop("username")
    session.pop("email")
    session.pop("level")
    session.pop("status")
    session.pop("prodi")
    flash("Logout success")
    return redirect(url_for("login"))


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "GET":
        if "username" in session:
            flash("You are still logged in. Please logout before sign up")
            return redirect(url_for("home"))
        else:
            session["status"] = "inactive"
            return render_template("signup.html", daftar_fakultas=daftar_fakultas, daftar_prodi=daftar_prodi
                                   , length=length)
    else:
        email = request.form["email"]
        username = request.form["username"]
        password = encrypt_string(request.form["password"])
        level = request.form["level"]
        prodi_sgnp = request.form["prodi"]
        session["email"] = email
        new_user = User(email, username, password, level, prodi_sgnp)
        db.session.add(new_user)
        db.session.commit()
        flash("Signup success")
        return redirect(url_for("login"))


@app.route("/soal", methods=["POST", "GET"])
def soal():
    if request.method == "GET":
        if "username" in session:
            username = session["username"]
            prodi_soal = session["prodi"]
            return render_template("soal.html", username=username, kriteria=kriteria, id_kriteria=id_kriteria, prodi=prodi_soal)
        else:
            session["status"] = "inactive"
            flash("Please login first")
            return redirect(url_for("login"))
    else:
        username_kaprodi = session["username"]
        prodi = session["prodi"]
        nilai = request.form.getlist('id_kriteria')
        if len(nilai) != 7:
            flash("Penilaian belum lengkap, silahkan isi kembali")
            return redirect(url_for("soal"))
        else:
            save = ','.join(nilai)
            borang = Borang(save, username_kaprodi, prodi)
            skor = 0.0
            for x in range(7):
                skor += (float(nilai[x]) * presentasi[x])
            hasil = Skor(prodi, skor)
            db.session.add(hasil)
            db.session.add(borang)
            db.session.commit()
            flash("Penilaian telah tersimpan")
            return redirect(url_for("soal"))


@app.route("/akreditasi")
def akreditasi():
    if "status" in session:
        if session["status"] == "active":
            username = session["username"]
            skor = Skor.query.all()
            length = len(skor)
            return render_template("akreditasi.html", skor=skor, length=length, username=username)
        else:
            flash("You are not logged in yet")
            return redirect(url_for("login"))
    else:
        session["status"] = "inactive"
        flash("You are not logged in yet")
        return redirect(url_for("login"))


@app.route("/akun")
def akun():
    if "status" in session:
        if session["status"] == "active":
            username = session["username"]
            found_user = User.query.filter_by(username=username).first()
            email = found_user.email
            level = found_user.level
            prodi = found_user.prodi
            return render_template("akun.html", username=username, email=email, level=level, prodi=prodi)
        else:
            flash("You are not logged in yet")
            return redirect(url_for("login"))
    else:
        session["status"] = "inactive"
        flash("You are not logged in yet")
        return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
    db.create_all()
