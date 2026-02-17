from datetime import datetime

from .extensions import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    unidad = db.Column(db.String(30), nullable=False)
    cantidad = db.Column(db.Float, default=0)
    categoria = db.Column(db.String(50), nullable=True)
    ubicacion = db.Column(db.String(100), nullable=True)

    movimientos = db.relationship(
        "Movimiento",
        back_populates="producto",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    @property
    def stock_actual(self):

        entradas = (
            self.movimientos.filter_by(tipo="entrada")
            .with_entities(db.func.sum(Movimiento.cantidad))
            .scalar()
            or 0
        )

        salidas = (
            self.movimientos.filter_by(tipo="salida")
            .with_entities(db.func.sum(Movimiento.cantidad))
            .scalar()
            or 0
        )

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
    telefono = db.Column(db.String(30), nullable=True)
    cif = db.Column(db.String(20), nullable=True)
    notas = db.Column(db.Text, nullable=True)

    movimientos = db.relationship(
        "Movimiento", back_populates="proveedor", lazy="dynamic"
    )
    pedidos_compra = db.relationship(
        "PedidoCompra", back_populates="proveedor", lazy="dynamic", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Proveedor {self.nombre}>"


class PedidoCompra(db.Model):
    __tablename__ = "pedidos_compra"

    id = db.Column(db.Integer, primary_key=True)
    proveedor_id = db.Column(db.Integer, db.ForeignKey("proveedores.id"), nullable=False)
    fecha_pedido = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    fecha_recepcion_esperada = db.Column(db.DateTime, nullable=True)
    fecha_recepcion_real = db.Column(db.DateTime, nullable=True)
    estado = db.Column(
        db.String(50), default="pendiente", nullable=False
    )  # ej. 'pendiente', 'recibido parcial', 'recibido completo', 'cancelado'
    total_amount = db.Column(db.Float, default=0.0, nullable=False)
    referencia = db.Column(db.String(120), nullable=True)
    observaciones = db.Column(db.Text, nullable=True)

    proveedor = db.relationship("Proveedor", back_populates="pedidos_compra")
    lineas = db.relationship(
        "LineaPedidoCompra",
        back_populates="pedido",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<PedidoCompra {self.id} - {self.proveedor.nombre if self.proveedor else 'N/A'} - {self.estado}>"


class LineaPedidoCompra(db.Model):
    __tablename__ = "lineas_pedido_compra"

    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey("pedidos_compra.id"), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    cantidad_pedida = db.Column(db.Float, nullable=False)
    cantidad_recibida = db.Column(db.Float, default=0.0, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, default=0.0, nullable=False)
    observaciones = db.Column(db.Text, nullable=True)

    pedido = db.relationship("PedidoCompra", back_populates="lineas")
    producto = db.relationship("Product")

    def __repr__(self):
        return f"<LineaPedidoCompra {self.id} - Producto: {self.producto.nombre if self.producto else 'N/A'} - Cantidad: {self.cantidad_recibida}>"


class CategoriaTransaccion(db.Model):
    __tablename__ = "categorias_transaccion"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    tipo = db.Column(db.String(10), nullable=False)  # 'ingreso' or 'gasto'

    transacciones = db.relationship(
        "Transaccion",
        back_populates="categoria",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<CategoriaTransaccion {self.nombre} ({self.tipo})>"


class Transaccion(db.Model):
    __tablename__ = "transacciones"

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(10), nullable=False)  # 'ingreso' or 'gasto'
    cantidad = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey("categorias_transaccion.id"), nullable=False)

    categoria = db.relationship("CategoriaTransaccion", back_populates="transacciones")

    def __repr__(self):
        return f"<Transaccion {self.tipo} {self.cantidad} ({self.fecha.strftime('%Y-%m-%d')})>"
