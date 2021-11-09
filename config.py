import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config():
    REGISTERED_USERS = {
    'kevinb@codingtemple.com':{"name":"Kevin","password":"abc123"},
    'alext@codingtemple.com':{"name":"Alex","password":"Colt45"},
    'joelc@codingtemple.com':{"name":"Joel","password":"MorphinTime"}
    }
    
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-definately-not-guess"
    SQLALCHEMY_DATABASE_URI= os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS= os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')