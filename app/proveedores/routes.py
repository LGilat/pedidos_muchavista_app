from flask import flash, redirect, render_template, request, url_for

from ..extensions import db
from ..models import Movimiento, Proveedor
from . import proveedores_bp


@proveedores_bp.route("/", methods=["GET"])
def lista_proveedores():
    proveedores = Proveedor.query.order_by(Proveedor.nombre).all()
    return render_template("proveedores/lista.html", proveedores=proveedores)


@proveedores_bp.route("/nuevo", methods=["GET", "POST"])
def nuevo_proveedor():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()

        if not nombre:
            flash("El nombre es obligatorio", "warning")
            return redirect(request.url)

        prov = Proveedor(
            nombre=nombre,
            telefono=request.form.get("telefono"),
            cif=request.form.get("cif"),
            notas=request.form.get("notas"),
        )

        db.session.add(prov)
        db.session.commit()
        flash("Proveedor creado correctamente", "success")
        return redirect(url_for("proveedores.lista_proveedores"))

    return render_template("proveedores/form.html")


@proveedores_bp.route("/<int:proveedor_id>/editar", methods=["GET", "POST"])
def editar_proveedor(proveedor_id):
    proveedor = Proveedor.query.get_or_404(proveedor_id)

    if request.method == "POST":
        proveedor.nombre = request.form.get("nombre", "").strip()
        proveedor.telefono = request.form.get("telefono")
        proveedor.cif = request.form.get("cif")
        proveedor.notas = request.form.get("notas")

        db.session.commit()
        flash("Proveedor actualizado correctamente", "success")
        return redirect(url_for("proveedores.lista_proveedores"))

    return render_template("proveedores/form.html", proveedor=proveedor)


@proveedores_bp.route("/<int:proveedor_id>/movimientos")
def movimientos_proveedor(proveedor_id):
    proveedor = Proveedor.query.get_or_404(proveedor_id)

    movimientos = proveedor.movimientos.order_by(Movimiento.fecha.desc()).all()

    return render_template(
        "proveedores/movimientos.html", proveedor=proveedor, movimientos=movimientos
    )
