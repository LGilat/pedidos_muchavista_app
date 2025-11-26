from flask import Blueprint

inventario_bp = Blueprint(
    "inventario",
    __name__,
    template_folder="../templates/inventario",
    static_folder="../static"
)

from . import routes
