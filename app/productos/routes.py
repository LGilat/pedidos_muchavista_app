from flask import render_template, redirect, url_for, request, flash
from . import productos_bp
from ..extensions import db
from ..models import Product
from .forms import ProductoForm

@productos_bp.route("/", methods=["GET","POST"])
@productos_bp.route("/")
def lista_productos():
    productos = Product.query.order_by(Product.nombre).all()

    # Obtener las categorías únicas que existen en la base de datos
    categorias = sorted({p.categoria for p in productos if p.categoria})

    return render_template("productos/list.html", productos=productos, categorias=categorias)

@productos_bp.route("/nuevo", methods=["GET", "POST"])
def nuevo_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        p = Product(
            nombre=form.nombre.data.strip(),
            unidad=form.unidad.data.strip(),
            cantidad=form.cantidad.data or 0,
            categoria=form.categoria.data.strip() or None
        )
        db.session.add(p)
        db.session.commit()
        flash("Producto creado", "success")
        return redirect(url_for("productos.lista_productos"))
    return render_template("productos/form.html", form=form, accion="Nuevo")

@productos_bp.route("/editar/<int:product_id>", methods=["GET", "POST"])
def editar_producto(product_id):
    p = Product.query.get_or_404(product_id)
    form = ProductoForm(obj=p)
    if form.validate_on_submit():
        p.nombre = form.nombre.data.strip()
        p.unidad = form.unidad.data.strip()
        p.cantidad = form.cantidad.data or 0
        p.categoria = form.categoria.data.strip() or None
        db.session.commit()
        flash("Producto actualizado", "success")
        return redirect(url_for("productos.lista_productos"))
    return render_template("productos/form.html", form=form, accion="Editar")

@productos_bp.route("/borrar/<int:product_id>", methods=["POST"])
def borrar_producto(product_id):
    p = Product.query.get_or_404(product_id)
    db.session.delete(p)
    db.session.commit()
    flash("Producto eliminado", "warning")
    return redirect(url_for("productos.lista_productos"))
