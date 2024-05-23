from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user
from flask_bcrypt import Bcrypt 

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


db.init_app(app)
bcrypt = Bcrypt(app) 

with app.app_context():
	db.create_all()


#jinja fungtions
def bitwise_and(a, b):
    return int(a) & int(b)

app.jinja_env.filters['bitwise_and'] = bitwise_and

@login_manager.user_loader
def loader_user(user_id):
	return Users.query.get(user_id)






if __name__ == "__main__":
	app.run()