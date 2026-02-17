from flask import Blueprint

bp = Blueprint("pedidos_compra", __name__, url_prefix="/pedidos_compra")

from . import routes  # noqa: F401
