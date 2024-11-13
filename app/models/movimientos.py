from app.utils.db import ConexMysql
from collections import OrderedDict
from datetime import datetime

class Movimiento:
    def __init__(self, movimiento_id=None, producto_id=None, fecha=None, concepto=None, cantidad=None):
        self.movimiento_id = movimiento_id
        self.producto_id = producto_id
        self.fecha = fecha
        self.concepto = concepto
        self.cantidad = cantidad

    @staticmethod
    def alive():
        data = OrderedDict([
            ("status", "Connection ok!"),
            ("message", "Movimientos alive"),
        ])
        return data

    @staticmethod
    def buscar_movimientos():
        con = ConexMysql()
        cursor = con.cursor()
        query = "SELECT * FROM movimientos"
        cursor.execute(query)
        resultados = cursor.fetchall()
        movimientos_items = []
        for movimiento in resultados:
            item = {
                'movimiento_id':        movimiento[0],
                'producto_id':          movimiento[1],
                'fecha': movimiento[2].strftime('%Y-%m-%d'),
                'concepto':             movimiento[3],
                'cantidad':             movimiento[4],
            }
            movimientos_items.append(item)
        cursor.close()
        return movimientos_items

    @staticmethod
    def buscar_movimiento_id(id_movimiento):
        con = ConexMysql()
        cursor = con.cursor()
        query = "SELECT * FROM movimientos WHERE movimiento_id = %s"
        cursor.execute(query, (id_movimiento,))
        movimiento = cursor.fetchone()
        if movimiento:
            item = {
                'movimiento_id':        movimiento[0],
                'producto_id':          movimiento[1],
                'fecha': movimiento[2].strftime('%Y-%m-%d'),
                'concepto':             movimiento[3],
                'cantidad':             movimiento[4],
            }
        else:
            item = {"error": "Movimiento no encontrado"}
        cursor.close()
        return item

    @staticmethod
    def agregar_movimiento(producto_id, fecha, concepto, cantidad):
        con = ConexMysql()
        cursor = con.cursor()
        fecha_formateada = datetime.strptime(fecha, "%Y-%m-%d").date()
        query = """
                INSERT INTO movimientos (producto_id, fecha, concepto, cantidad)
                VALUES (%s, %s, %s, %s)
                """
        cursor.execute(query, (producto_id, fecha_formateada, concepto, cantidad))
        con.commit()
        movimiento_id = cursor.lastrowid
        cursor.close()
        return {"movimiento_id": movimiento_id, "status": "Movimiento agregado exitosamente"}

    @staticmethod
    def modificar_movimiento_id(movimiento_id, producto_id, fecha, concepto, cantidad):
        con = ConexMysql()
        cursor = con.cursor()
        fecha_formateada = datetime.strptime(fecha, "%Y-%m-%d").date()
        query = """
                UPDATE movimientos
                SET producto_id = %s, fecha = %s, concepto = %s, cantidad = %s
                WHERE movimiento_id = %s
                """
        cursor.execute(query, (producto_id, fecha_formateada, concepto, cantidad, movimiento_id))
        con.commit()
        rows_affected = cursor.rowcount
        cursor.close()
        if rows_affected > 0:
            return {"status": "Movimiento modificado exitosamente"}
        else:
            return {"error": "Movimiento no encontrado"}

    @staticmethod
    def eliminar_movimiento_id(movimiento_id):
        con = ConexMysql()
        cursor = con.cursor()
        query = "DELETE FROM movimientos WHERE movimiento_id = %s"
        cursor.execute(query, (movimiento_id,))
        con.commit()
        rows_affected = cursor.rowcount
        cursor.close()
        if rows_affected > 0:
            return {"status": "Movimiento eliminado exitosamente"}
        else:
            return {"error": "Movimiento no encontrado"}
