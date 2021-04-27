from flask_login import LoginManager
from flask_ckeditor import CKEditor
from database import MySQL
from flask_wtf.csrf import CSRFProtect

db = MySQL()
login_manager = LoginManager()
ck = CKEditor()
csrf = CSRFProtect()

login_manager.login_view = "auth.login"
login_manager.login_message_category = "info"
login_manager.login_message = "Vennligst logg inn for å se denne siden."
