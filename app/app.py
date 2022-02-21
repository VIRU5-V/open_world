import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_login import LoginManager 


db = SQLAlchemy()
migrate = Migrate()
admin = Admin(name='microblog', template_mode='bootstrap4')
login_manager = LoginManager()
login_manager.login_view = 'auth_blueprint.login'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'this is secret key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///open_world.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static\pictures')
    app.config['FLASK_ADMIN_SWATCH'] = 'Lux'

    # app.config['FLASK_ADMIN_SWATCH'] = 'paper'
    db.init_app(app)
    migrate.init_app(app, db)
    admin.init_app(app)
    login_manager.init_app(app)



    # routes
    from .main.views import main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth.views import auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    return app