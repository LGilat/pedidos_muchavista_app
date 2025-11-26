from flask import render_template, request, redirect, url_for, jsonify, flash
from . import inventario_bp
from ..models import Product
from ..extensions import db

@inventario_bp.route("/", methods=["GET"])
def ver_inventario():
    # opcionalmente filtrar por categoria o búsqueda con query params
    categoria = request.args.get("categoria")
    q = request.args.get("q")
    query = Product.query
    if categoria:
        query = query.filter_by(categoria=categoria)
    if q:
        query = query.filter(Product.nombre.ilike(f"%{q}%"))
    productos = query.order_by(Product.nombre).all()
    # enviamos productos a la vista tipo tarjetas
    return render_template("inventario/index.html", productos=productos)

@inventario_bp.route("/update/<int:product_id>", methods=["POST"])
def update_producto(product_id):
    """
    Actualiza la cantidad de un producto.
    Espera form data: 'cantidad' (float) o 'delta' (int) para +/-.
    Retorna JSON si es petición AJAX, si no redirige.
    """
    p = Product.query.get_or_404(product_id)
    # prioridad: delta (para +/-), sino cantidad absoluta
    if 'delta' in request.form:
        try:
            delta = float(request.form.get('delta', 0))
        except ValueError:
            delta = 0
        p.cantidad = (p.cantidad or 0) + delta
    elif 'cantidad' in request.form:
        try:
            p.cantidad = float(request.form.get('cantidad', p.cantidad or 0))
        except ValueError:
            pass
    db.session.commit()

    # Si es AJAX devolvemos JSON
    if request.is_json or request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({"ok": True, "id": p.id, "cantidad": p.cantidad})
    flash(f"Cantidad de {p.nombre} actualizada", "success")
    return redirect(url_for("inventario.ver_inventario"))

@inventario_bp.route("/guardar_todo", methods=["POST"])
def guardar_todo():
    """
    Recibe pares product_id -> cantidad en el form y guarda todo.
    Útil para el botón 'Guardar todo' de la UI.
    """
    data = request.form
    cambios = 0
    for key, value in data.items():
        if key.startswith("cantidad_"):
            try:
                pid = int(key.split("_",1)[1])
                qty = float(value)
                p = Product.query.get(pid)
                if p:
                    p.cantidad = qty
                    cambios += 1
            except Exception:
                continue
    db.session.commit()
    flash(f"{cambios} productos actualizados", "success")
    return redirect(url_for("inventario.ver_inventario"))
