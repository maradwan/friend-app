from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@xxx.rds.amazonaws.com/friend?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
  __tablename__ = 'users'
  uid = db.Column(db.Integer, primary_key = True)
  firstname = db.Column(db.String(100))
  lastname = db.Column(db.String(100))
  email = db.Column(db.String(120), unique=True)
  pwdhash = db.Column(db.String(120))
  friends_users = db.relationship('Friends', backref='owner', lazy='dynamic')

  def __init__(self, firstname, lastname, email, password):
    self.firstname = firstname.title()
    self.lastname = lastname.title()
    self.email = email.lower()
    self.set_password(password)

  def set_password(self, password):
    self.pwdhash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.pwdhash, password)

class Friends(db.Model):
  __tablename__ = 'friends'
  f_id = db.Column(db.Integer, primary_key = True)
  f_firstname = db.Column(db.String(100))
  f_lastname = db.Column(db.String(100))
  f_email = db.Column(db.String(120))
  f_phone = db.Column(db.String(120))
  user_id = db.Column(db.Integer, db.ForeignKey('users.uid', ondelete='CASCADE'),nullable=False)
  users = db.relationship('User')

  def __init__(self, f_firstname, f_lastname, f_email, f_phone, user_id):
    self.f_firstname = f_firstname
    self.f_lastname = f_lastname
    self.f_email = f_email
    self.f_phone = f_phone
    self.user_id = user_id
