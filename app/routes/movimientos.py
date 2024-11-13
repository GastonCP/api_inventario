from flask import Blueprint, Response, request, jsonify
from app.models.movimientos import Movimiento
import json

bp_m = Blueprint('movimientos', __name__, url_prefix='/movimientos')

@bp_m.route('/alive', methods=['GET'])
def dir_alive():
    data = Movimiento.alive()
    return Response(json.dumps(data), mimetype='application/json')

@bp_m.route('/all', methods=['GET'])
def dir_obtener_movimientos():
    data = Movimiento.buscar_movimientos()
    return Response(json.dumps(data), mimetype='application/json')

@bp_m.route('/<int:movimiento_id>', methods=['GET'])
def dir_buscar_movimiento_id(movimiento_id):
    data = Movimiento.buscar_movimiento_id(movimiento_id)
    return Response(json.dumps(data), mimetype='application/json')

@bp_m.route('/', methods=['POST'])
def dir_agregar_movimiento():
    datos = request.get_json()
    producto_id = datos.get('producto_id')
    fecha = datos.get('fecha')
    concepto = datos.get('concepto')
    cantidad = datos.get('cantidad')
    if not all([producto_id, fecha, concepto, cantidad]):
        return jsonify({"error": "Todos los campos son obligatorios"}), 400
    resultado = Movimiento.agregar_movimiento(producto_id, fecha, concepto, cantidad)
    return jsonify(resultado), 201

@bp_m.route('/<int:movimiento_id>', methods=['PUT'])
def dir_modificar_movimiento(movimiento_id):
    datos = request.get_json()
    producto_id = datos.get('producto_id')
    fecha = datos.get('fecha')
    concepto = datos.get('concepto')
    cantidad = datos.get('cantidad')
    if not all([producto_id, fecha, concepto, cantidad]):
        return jsonify({"error": "Todos los campos son obligatorios"}), 400
    resultado = Movimiento.modificar_movimiento_id(movimiento_id, producto_id, fecha, concepto, cantidad)
    return jsonify(resultado), 200 if "status" in resultado else 404

@bp_m.route('/<int:movimiento_id>', methods=['DELETE'])
def dir_eliminar_movimiento(movimiento_id):
    resultado = Movimiento.eliminar_movimiento_id(movimiento_id)
    return jsonify(resultado), 200 if "status" in resultado else 404