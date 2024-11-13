from flask_mysqldb import MySQL

mysql = MySQL()

def init_app(app):
    app.config['MYSQL_HOST'] = app.config.get('MYSQL_HOST')
    app.config['MYSQL_USER'] = app.config.get('MYSQL_USER')
    app.config['MYSQL_PASSWORD'] = app.config.get('MYSQL_PASS')
    app.config['MYSQL_DB'] = app.config.get('MYSQL_DB')
    mysql.init_app(app)

def ConexMysql():
    return mysql.connection
