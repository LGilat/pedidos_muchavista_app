from flask import Blueprint

from flask import Blueprint

# NO pongas template_folder ni static_folder aquí
productos_bp = Blueprint("productos", __name__)

from . import routes
