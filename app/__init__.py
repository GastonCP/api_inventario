from flask import Flask
from app.routes import productos, movimientos
from app.utils.db import init_app


def crear_app():
    app = Flask(__name__)
    app.config.from_object('app.configs.ConfigDB')

    init_app(app)
    app.register_blueprint(productos.bp_p)
    app.register_blueprint(movimientos.bp_m)
    return app