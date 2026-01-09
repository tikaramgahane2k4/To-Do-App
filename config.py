import os

SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "postgresql://student_ms_db_1i7f_user:oGpNiDNenVW5TjjLWOba66hcMtd3YqG0@dpg-d57c6peuk2gs73cvb8qg-a.oregon-postgres.render.com/To-Do data db"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.environ.get("SECRET_KEY", "TODOS123_SECRET_KEY_CHANGE_IN_PRODUCTION")
SESSION_TYPE = "filesystem"
PERMANENT_SESSION_LIFETIME = 86400

