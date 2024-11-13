from flask import Blueprint, Response, request, jsonify
from app.models.productos import Producto
import json

bp_p = Blueprint('productos', __name__, url_prefix='/productos')

@bp_p.route('/alive', methods=['GET'])
def dir_alive():
    data = Producto.alive()
    return Response(json.dumps(data), mimetype='application/json')

@bp_p.route('/all', methods=['GET'])
def dir_obtener_productos():
    data = Producto.buscar_productos()
    return Response(json.dumps(data), mimetype='application/json')

@bp_p.route('/<int:id_producto>', methods=['GET'])
def dir_buscar_producto_id(id_producto):
    data = Producto.buscar_producto_id(id_producto)
    return Response(json.dumps(data), mimetype='application/json')

@bp_p.route('/', methods=['POST'])
def dir_agregar_producto():
    datos = request.get_json()
    nombre = datos.get('nombre')
    precio_por_unidad = datos.get('precio_por_unidad')
    unidad_de_medicion = datos.get('unidad_de_medicion')
    stock_minimo = datos.get('stock_minimo')
    detalles = datos.get('detalles')
    if not all([nombre, precio_por_unidad, unidad_de_medicion, stock_minimo, detalles]):
        return jsonify({"error": "Todos los campos son obligatorios"}), 400
    resultado = Producto.agregar_producto(nombre, precio_por_unidad, unidad_de_medicion, stock_minimo, detalles)
    return jsonify(resultado), 201

@bp_p.route('/<int:producto_id>', methods=['PUT'])
def dir_modificar_producto(producto_id):
    datos = request.get_json()
    nombre = datos.get('nombre')
    precio_por_unidad = datos.get('precio_por_unidad')
    unidad_de_medicion = datos.get('unidad_de_medicion')
    stock_minimo = datos.get('stock_minimo')
    detalles = datos.get('detalles')
    if not all([nombre, precio_por_unidad, unidad_de_medicion, stock_minimo, detalles]):
        return jsonify({"error": "Todos los campos son obligatorios"}), 400
    resultado = Producto.modificar_producto_id(producto_id, nombre, precio_por_unidad, unidad_de_medicion, stock_minimo, detalles)
    return jsonify(resultado), 200 if "status" in resultado else 404

@bp_p.route('/<int:producto_id>', methods=['DELETE'])
def dir_eliminar_producto(producto_id):
    resultado = Producto.eliminar_producto_id(producto_id)
    return jsonify(resultado), 200 if "status" in resultado else 404