from app import app
from hd_app.data_auth import reset_auth_database

with app.app_context():
    reset_auth_database()
