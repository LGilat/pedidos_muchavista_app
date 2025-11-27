from flask import Blueprint, render_template, redirect, url_for

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    # Redirige a la lista de productos
    return redirect(url_for("productos.lista_productos"))
    # O si quieres mostrar un index.html con botones:
    # return render_template("index.html")
