# Si Borang
Web Tubes
## Database (model/entity)
1. User
Atribut:
  - id_user: integer, primary key, auto increment
  - email: varchar(50)
  - username: varchar(50)
  - password: varchar(64)
  - level: varchar(14)
  - prodi: varchar(30), nullable
  
2. Borang
Atribut:
  - id_borang: integer, primary key, auto increment
  - isi: varchar(14)
  - username_kaprodi: varchar(50), nullable
  - prodinya: varchar(30), nullable
  
3. Skor
Atribut:
  - id_skor: integer, primary key, auto increment
  - prodinya: varchar(30)
  - skor: integer

## Cara run
1. Install python (pastikan sampai tambah environment variable): https://bitnesia.com/bagaimana-cara-install-python-di-windows-10.html
2. Install flask: https://www.codepolitan.com/menjadi-developer-web-dengan-python-dan-flask-hello-world-5a3b1af29b052
3. Install sqlalchemy: https://pypi.org/project/Flask-SQLAlchemy/
4. Buka direktori project siborang dengan cmd: https://smkvinama2tkj.blogspot.com/2012/10/mungkin-yang-namanya-cmd-command-prompt.html
5. Pada cmd, run command "python flask_app.py" atau "python3 flask_app.py" untuk python3
