from flask import Blueprint

movimientos_bp = Blueprint("movimientos", __name__, template_folder="../templates/movimientos")

from . import routes  # noqa
