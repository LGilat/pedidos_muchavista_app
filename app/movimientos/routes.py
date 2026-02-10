from datetime import datetime

from flask import flash, redirect, render_template, request, url_for

from ..extensions import db
from ..models import Movimiento, Product, Proveedor
from . import movimientos_bp


@movimientos_bp.route("/entradas", methods=["GET", "POST"])
def registrar_entradas():
    productos = Product.query.order_by(Product.nombre).all()
    proveedores = Proveedor.query.order_by(Proveedor.nombre).all()
    if request.method == "POST":
        # Metadatos del albarán
        referencia = request.form.get("referencia", "").strip()
        proveedor_id = request.form.get("proveedor_id", "").strip()
        fecha_raw = request.form.get("fecha")
        proveedor = None
        if proveedor_id:
            try:
                proveedor = Proveedor.query.get_or_404(int(proveedor_id))
            except ValueError:
                proveedor = None
        try:
            proveedor_id = int(proveedor_id)
        except ValueError:
            print("Error en el proveedor_id al pasar a int")
        if not proveedor_id:
            flash("Debes seleccionar un proveedor")
            return redirect(url_for("movimientos.registrar_entradas"))

        try:
            fecha = (
                datetime.fromisoformat(fecha_raw) if fecha_raw else datetime.utcnow()
            )
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
                    referencia=f"{referencia} | {proveedor}"
                    if referencia or proveedor
                    else referencia or proveedor,
                    proveedor_id=proveedor_id if proveedor else None,
                )
                db.session.add(mov)
                any_added = True

        if any_added:
            db.session.commit()
            flash("Entradas registradas correctamente.", "success")
        else:
            flash("No se han detectado cantidades positivas. Nada que guardar.", "info")

        return redirect(url_for("productos.lista_productos"))

    return render_template(
        "movimientos/entradas.html", productos=productos, proveedores=proveedores
    )


@movimientos_bp.route("/historico", methods=["GET"])
def historico_movimientos():
    # Filtros
    producto_id = request.args.get("producto_id", type=int)
    proveedor_id = request.args.get("proveedor_id", type=int)
    tipo = request.args.get("tipo", default="")
    fecha_inicio = request.args.get("fecha_inicio")
    fecha_fin = request.args.get("fecha_fin")

    query = Movimiento.query.join(Product).outerjoin(Proveedor)

    if producto_id:
        query = query.filter(Movimiento.producto_id == producto_id)
    if proveedor_id:
        query = query.filter(Movimiento.proveedor_id == proveedor_id)
    if tipo in ("entrada", "salida"):
        query = query.filter(Movimiento.tipo == tipo)
    if fecha_inicio:
        try:
            inicio = datetime.fromisoformat(fecha_inicio)
            query = query.filter(Movimiento.fecha >= inicio)
        except:
            pass
    if fecha_fin:
        try:
            fin = datetime.fromisoformat(fecha_fin)
            query = query.filter(Movimiento.fecha <= fin)
        except:
            pass

    movimientos = query.order_by(Movimiento.fecha.desc()).all()
    productos = Product.query.order_by(Product.nombre).all()
    proveedores = Proveedor.query.order_by(Proveedor.nombre).all()

    return render_template(
        "movimientos/historico.html",
        movimientos=movimientos,
        productos=productos,
        proveedores=proveedores,
        filtros=request.args,
    )
