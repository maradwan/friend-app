from flask import Flask

app = Flask(__name__)

app.secret_key = 'Sg4NbQpvhCzh2c4yas53bXznN8jazmk59hg28JC7BDceRxQhDFStFvN6zsFj3NVgjH64nrrTvcXzYrTg'

app.config["MAIL_SERVER"] = "127.0.0.1"
app.config["MAIL_PORT"] = 25
app.config["MAIL_USE_SSL"] = False
#app.config["MAIL_USERNAME"] = ''
#app.config["MAIL_PASSWORD"] = ''

from routes import mail
mail.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@xxx.rds.amazonaws.com/friend?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


from models import db
db.init_app(app)
db.create_all()


import friend.routes
