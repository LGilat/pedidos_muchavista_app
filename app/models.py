from .extensions import db
from datetime import datetime

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    unidad = db.Column(db.String(30), nullable=False)
    cantidad = db.Column(db.Float, default=0)
    categoria = db.Column(db.String(50), nullable=True)
    
    movimientos = db.relationship(
        "Movimiento",
        back_populates="producto",
        lazy="dynamic",
        cascade="all, delete-orphan"
    )

    @property
    def stock_actual(self):
        
        entradas = self.movimientos.filter_by(tipo="entrada").with_entities(
            db.func.sum(Movimiento.cantidad)
        ).scalar() or 0

        salidas = self.movimientos.filter_by(tipo="salida").with_entities(
            db.func.sum(Movimiento.cantidad)
        ).scalar() or 0

        return float(entradas) - float(salidas)





class Movimiento(db.Model):
    __tablename__ = "movimientos"

    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    
    proveedor_id = db.Column(db.Integer, db.ForeignKey("proveedores.id"), nullable=True)
    
    tipo = db.Column(db.String(10), nullable=False)  # "entrada" | "salida"
    cantidad = db.Column(db.Float, nullable=False, default=0)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    referencia = db.Column(db.String(120), nullable=True)  # número albarán / nota
    
    producto = db.relationship("Product", back_populates="movimientos")
    proveedor = db.relationship("Proveedor", back_populates="movimientos")

    def __repr__(self):
        return f"<Movimiento {self.tipo} {self.cantidad} de {self.producto_id}>"


class Proveedor(db.Model):
    __tablename__ = "proveedores"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False, unique=True)

    movimientos = db.relationship("Movimiento", back_populates="proveedor")

    def __repr__(self):
        return f"<Proveedor {self.nombre}>"
