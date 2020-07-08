from flask import Flask
from flask_bootstrap Bootstrap
from flask_mail import Mail
from flaskext.mysql import MySQL
from config import config

bootstrap = Bootstrap()
mail = Mail()
db = MySQL()

def create_app(config_name):
    booky = Flask(__name__)
    booky.config.from_object(config[config_name])
    config[config_name]init_app(booky)

    bootstrap.init_app(booky)
    main.init_app(booky)
    db.init_app(booky)

    from .main import main as main_blueprint
    booky.register_blueprint(main_blueprint)

    return booky
