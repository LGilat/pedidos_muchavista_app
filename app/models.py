from .extensions import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    unidad = db.Column(db.String(30), nullable=False)
    cantidad = db.Column(db.Float, default=0)
    categoria = db.Column(db.String(50), nullable=True)
