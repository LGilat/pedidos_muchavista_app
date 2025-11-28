from flask import Flask
from .config import Config
from .extensions import db, migrate, csrf
from .productos import productos_bp
from .inventario import inventario_bp
from .services   import export_bp
from .routes import main_bp


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    app.register_blueprint(main_bp);
    app.register_blueprint(productos_bp, url_prefix="/productos")
    app.register_blueprint(export_bp, url_prefix="/exportar")
    #app.register_blueprint(inventario_bp, url_prefix="/inventario")
    return app
