import os
from flask import Flask
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__, static_url_path = '', static_folder='../public')

app.config.update(SEND_FILE_MAX_AGE_DEFAULT=0)
# any strange string here - this is key to generate tokens
app.config.update(SECRET_KEY='sadfwerusafgr-sesfgfgcret-jdddh')
app.config.update(BASEDIR=os.path.abspath(os.path.dirname(__file__)))
app.config.update(JWT_EXPIRATION_DELTA=timedelta(seconds=129600))

app.wsgi_app = ProxyFix(app.wsgi_app)
from app import views
