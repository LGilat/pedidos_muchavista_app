from flask import render_template, request, redirect, url_for, flash
from . import movimientos_bp
from ..extensions import db
from ..models import Product, Movimiento, Proveedor
from datetime import datetime

@movimientos_bp.route("/entradas", methods=["GET", "POST"])
def registrar_entradas():
    productos = Product.query.order_by(Product.nombre).all()
    proveedores = Proveedor.query.order_by(Proveedor.nombre).all();

    if request.method == "POST":
        # Metadatos del albarán
        referencia = request.form.get("referencia", "").strip()
        proveedor_id = request.form.get("proveedor_id", "").strip()
        fecha_raw = request.form.get("fecha")
        proveedor = None;
        if proveedor_id:
            try:
                proveedor = Proveedor.query.get_or_404(int(proveedor_id))
            except ValueError:
                proveedor=None;
        try:
            proveedor_id = int(proveedor_id)
        except ValueError:
            print("Error en el proveedor_id al pasar a int");
        if not proveedor_id:
            flash("Debes seleccionar un proveedor");
            return redirect(url_for('movimientos.registrar_entradas'))
        
        try:
            fecha = datetime.fromisoformat(fecha_raw) if fecha_raw else datetime.utcnow()
        except:
            fecha = datetime.utcnow()

        ids = request.form.getlist("id[]")
        cantidades = request.form.getlist("qty[]")

        any_added = False
        for prod_id, qty_str in zip(ids, cantidades):
            try:
                qty = float(qty_str) if qty_str not in (None, "") else 0
            except:
                qty = 0

            if qty and qty > 0:
                mov = Movimiento(
                    producto_id=int(prod_id),
                    tipo="entrada",
                    cantidad=qty,
                    fecha=fecha,
                    referencia=f"{referencia} | {proveedor}" if referencia or proveedor else referencia or proveedor,
                    proveedor_id=proveedor_id if proveedor else None
                )
                db.session.add(mov)
                any_added = True

        if any_added:
            db.session.commit()
            flash("Entradas registradas correctamente.", "success")
        else:
            flash("No se han detectado cantidades positivas. Nada que guardar.", "info")

        return redirect(url_for("productos.lista_productos"))

    return render_template("movimientos/entradas.html", productos=productos, proveedores=proveedores)
