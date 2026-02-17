from flask import Blueprint

bp = Blueprint("contabilidad", __name__, url_prefix="/contabilidad")

from . import routes  # noqa: F401
