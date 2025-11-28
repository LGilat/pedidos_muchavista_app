from flask import Blueprint


# NO pongas template_folder ni static_folder aquí
export_bp = Blueprint('export', __name__)

from . import routes