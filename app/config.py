import os

class Config:
    SECRET_KEY = "super-secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///inventario.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
