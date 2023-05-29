from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__, static_url_path='/static')
    # key for cookie auth
    # app.config['SECRET KEY'] = 'asdf'
    app.config.from_object(Config)
    from .views import views
    app.register_blueprint(views, url_prefix='/')
    return app

