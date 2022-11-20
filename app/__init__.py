from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import cloudinary
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = '(@*$&!(*@&$(*!&@()%&*(!@*%&(*!@&##)(!@$&(!@$&*^!@*(&$^@!&*^#!&*@#^*'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:01312101220LtfA@localhost/labsaledb?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['PAGE_SIZE'] = 4


db = SQLAlchemy(app=app)

cloudinary.config(
    cloud_name='dgyytgkae',
    api_key='573742567799544',
    api_secret='HZjhD-RMcxVk2-naTir65-nJYAE',
)
SESSION_COOKIE_SECURE = True

login = LoginManager(app=app)