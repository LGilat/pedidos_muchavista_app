from flask import Flask, render_template

from .config import Config
from .extensions import csrf, db, migrate
from .inventario import inventario_bp
from .movimientos import movimientos_bp
from .productos import productos_bp
from .proveedores import proveedores_bp
from .routes import main_bp
from .services import export_bp


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(403)
    def forbidden(e):
        return render_template("errors/403.html"), 403

    @app.errorhandler(500)
    def internal_error(e):
        db.session.rollback()
        return render_template("errors/500.html"), 500

    app.register_blueprint(main_bp)
    app.register_blueprint(productos_bp, url_prefix="/productos")
    app.register_blueprint(export_bp, url_prefix="/exportar")
    app.register_blueprint(movimientos_bp, url_prefix="/movimientos")
    app.register_blueprint(proveedores_bp, url_prefix="/proveedores")
    # app.register_blueprint(inventario_bp, url_prefix="/inventario")
    return app
