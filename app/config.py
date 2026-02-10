import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")
    SQLALCHEMY_DATABASE_URI = "sqlite:///inventario.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
