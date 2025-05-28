from flask_login import LoginManager
from flask_caching import Cache
from authlib.integrations.flask_client import OAuth

login_manager = LoginManager()
cache = Cache()
oauth = OAuth()