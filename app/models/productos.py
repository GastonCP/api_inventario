from app.utils.db import ConexMysql
from collections import OrderedDict

class Producto:
    def __init__(self, producto_id=None, nombre=None, precio_por_unidad=None, unidad_de_medicion=None, stock_minimo=None, detalles=None):
        self.producto_id = producto_id
        self.nombre = nombre
        self.precio_por_unidad = precio_por_unidad
        self.unidad_de_medicion = unidad_de_medicion
        self.stock_minimo = stock_minimo
        self.detalles = detalles

    @staticmethod
    def alive():
        data = OrderedDict([
            ("status", "Connection ok!"),
            ("message", "Productos alive"),
        ])
        return data

    @staticmethod
    def buscar_productos():
        con = ConexMysql()
        cursor = con.cursor()
        query = "SELECT * FROM productos"
        cursor.execute(query)
        resultados = cursor.fetchall()
        productos_items = []
        for producto in resultados:
            item = {
                'producto_id': producto[0],
                'nombre': producto[1],
                'precio_por_unidad': producto[2],
                'unidad_de_medicion': producto[3],
                'stock_minimo': producto[4],
                'detalles': producto[5],
            }
            productos_items.append(item)
        cursor.close()
        return productos_items

    @staticmethod
    def buscar_producto_id(id_producto):
        con = ConexMysql()
        cursor = con.cursor()
        query = "SELECT * FROM productos WHERE producto_id = %s"
        cursor.execute(query, (id_producto,))
        producto = cursor.fetchone()
        if producto:
            item = {
                'producto_id': producto[0],
                'nombre': producto[1],
                'precio_por_unidad': producto[2],
                'unidad_de_medicion': producto[3],
                'stock_minimo': producto[4],
                'detalles': producto[5],
            }
        else:
            item = {"error": "Producto no encontrado"}
        cursor.close()
        return item

    @staticmethod
    def agregar_producto(nombre, precio_por_unidad, unidad_de_medicion, stock_minimo, detalles):
        con = ConexMysql()
        cursor = con.cursor()
        query = """
                INSERT INTO productos (nombre, precio_por_unidad, unidad_de_medicion, stock_minimo, detalles)
                VALUES (%s, %s, %s, %s, %s)
                """
        cursor.execute(query, (nombre, precio_por_unidad, unidad_de_medicion, stock_minimo, detalles))
        con.commit()
        producto_id = cursor.lastrowid
        cursor.close()
        return {"producto_id": producto_id, "status": "Producto agregado exitosamente"}

    @staticmethod
    def modificar_producto_id(producto_id, nombre, precio_por_unidad, unidad_de_medicion, stock_minimo, detalles):
        con = ConexMysql()
        cursor = con.cursor()
        query = """
                UPDATE productos
                SET nombre = %s, precio_por_unidad = %s, unidad_de_medicion = %s, stock_minimo = %s, detalles = %s
                WHERE producto_id = %s
                """
        cursor.execute(query, (nombre, precio_por_unidad, unidad_de_medicion, stock_minimo, detalles, producto_id))
        con.commit()
        rows_affected = cursor.rowcount
        cursor.close()
        if rows_affected > 0:
            return {"status": "Producto modificado exitosamente"}
        else:
            return {"error": "Producto no encontrado"}

    @staticmethod
    def eliminar_producto_id(producto_id):
        con = ConexMysql()
        cursor = con.cursor()
        query = "DELETE FROM productos WHERE producto_id = %s"
        cursor.execute(query, (producto_id,))
        con.commit()
        rows_affected = cursor.rowcount
        cursor.close()
        if rows_affected > 0:
            return {"status": "Producto eliminado exitosamente"}
        else:
            return {"error": "Producto no encontrado"}
