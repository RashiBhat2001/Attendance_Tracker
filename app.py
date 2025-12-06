import os
import logging

from flask import Flask
from flask_login import LoginManager
from werkzeug.middleware.proxy_fix import ProxyFix

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class Student:
    def __init__(self, student_id, name):
        self.id = student_id
        self.student_id = student_id
        self.name = name
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False
    
    def get_id(self):
        return self.student_id

students_cache = {}

@login_manager.user_loader
def load_user(student_id):
    return students_cache.get(student_id)

from routes import *
