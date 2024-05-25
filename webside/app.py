from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user
from flask_bcrypt import Bcrypt 
from databace_conector import DataBase
import hashlib
from datetime import datetime


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SECRET_KEY"] = "abc"
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.init_app(app)


class Users(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(250), unique=True, nullable=False)
	password = db.Column(db.String(250), nullable=False)
	creds = db.Column(db.Integer, nullable=False)

storage_db = DataBase('database/storage.db')

db.init_app(app)
bcrypt = Bcrypt(app) 

with app.app_context():
	db.create_all()


#jinja filters
def bitwise_and(a, b):
    return int(a) & int(b)

app.jinja_env.filters['bitwise_and'] = bitwise_and

@login_manager.user_loader
def loader_user(user_id):
	return Users.query.get(user_id)

@app.route("/", methods=["GET", "POST"])
def index():
	if request.method == "POST":
		user = Users.query.filter_by(
			username=request.form.get("username")).first()
		if bcrypt.check_password_hash(user.password, request.form.get("password")):
			login_user(user)
			return redirect(url_for("menu"))
	return render_template('index.html')

@app.route("/menu")
def menu():
	return render_template('menu.html')

@app.route('/make_user', methods=["GET", "POST"])
def make_user():
	if request.method == "POST":
		user = Users(username=request.form.get("username"),
					password=bcrypt.generate_password_hash(request.form.get("password")).decode('utf-8'),
					creds=request.form.get("creds"))
		db.session.add(user)
		db.session.commit()
		return redirect(url_for("menu"))
	return render_template("make_user.html")

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for("index"))

@app.route("/scan")
def scan():
	return render_template("scan.html")

@app.route("/admin")
def admin():
	return render_template("admin.html")

@app.route("/opret_gest", methods=["GET", "POST"])
def opret_gest():
	if request.method == "POST":
		uid = f'{request.form.get("name")}{request.form.get("email")}{datetime.now()}'
		hashed_data = hashlib.md5(uid.encode())
		gest = (request.form.get("name"),request.form.get("email"),request.form.get("room"),hashed_data.hexdigest())
		print(gest)
		db_log = storage_db.add_to_databace('INSERT INTO gest (name, email, room, uid) VALUES(?, ?, ?, ?)',gest)
		if type(db_log) is str:
			split_log = db_log.split('.')
			return render_template("opret_gest.html",warn = f'{split_log[1].upper()} ALREADY IN USE')
		else:
			return render_template("opret_gest.html",warn = 'GUEST SUCCESFULLY CREATED')
	return render_template("opret_gest.html",warn = 'none')
	

if __name__ == "__main__":
	app.run()