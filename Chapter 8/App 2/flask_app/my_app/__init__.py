import os
from sqlalchemy import MetaData
from flask import Flask 
from flask_login import LoginManager
# from flask_mongoengine import MongoEngine
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from redis import Redis
file_path = os.path.abspath(os.getcwd()+'\test.db')
# create the extension

# create the app
app = Flask(__name__)


app.config['WTF_CSRF_SECRET_KEY'] = 'SOME_SECRET_KEY'
# app.config['MONGODB_SETTINGS'] = {'DB':'my_catalog'}
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config["UPLOAD_FOLDER"] = os.path.realpath('.') + '/my_app/static/uploads'
# initialize the app with the extension


convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(app, metadata=metadata)
app.secret_key = 'SOME_SECRET_KEY'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# db.init_app(app)

# db.init_all()
migrate = Migrate(app, db)
app.debug = True
# db = MongoEngine(app)
from my_app.auth.views import auth
app.register_blueprint(auth)
redis = Redis(host='localhost', port=6379)
with app.app_context():
    # db.drop_all()
    db.create_all()