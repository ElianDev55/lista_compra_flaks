from itertools import product
from flask import Flask , render_template, request , redirect , url_for, flash
from flask_mysqldb import MySQL

lista = Flask(__name__)

lista.config['MYSQL_HOST'] = 'localhost'
lista.config['MYSQL_USER'] = 'root'
lista.config['MYSQL_PASSWORD'] = ''
lista.config['MYSQL_DB'] = 'lista_compra'
mysql = MySQL(lista)

lista.secret_key= 'lista_secret_key'


@lista.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productos')
    data = cur.fetchall()
    return render_template('formu.html', productos = data)

@lista.route('/agregar', methods = ['POST'])
def agregar():
    if request.method == 'POST':
        nombre = request.form['nombre']
        cantidad = request.form['cantidad']
        supermercado = request.form['supermercado']
        cur = mysql.connection.cursor()
        cur.execute(' INSERT productos (nombre,cantidad,supermercado) VALUES (%s,%s,%s)',
        (nombre,cantidad,supermercado))
        mysql.connection.commit()
        flash('SE HA AGREGADO CON EXITO EL PRODUCTO A LA LISTA  ')
        return redirect(url_for('index') )


@lista.route('/editar/<string:id>')
def editar(id):
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM productos WHERE id = {id}")
    data = cur.fetchall()
    return render_template('editarlista.html', productos=data[0])

@lista.route('/actualizar/<string:id>', methods = ['POST'])
def actualizar(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        cantidad = request.form['cantidad']
        supermercado = request.form['supermercado']
        cur = mysql.connection.cursor()
        cur.execute("""
                UPDATE productos 
                SET nombre = %s,
                    cantidad = %s,
                    supermercado = %s
                WHERE id = %s
                """, (nombre,cantidad,supermercado,id))
        flash('SE HA EDITADO CON EXITO EL PRODUCTO  DE LA LISTA ')
        mysql.connection.commit()
        return redirect(url_for('index') )

@lista.route('/eliminar/<string:id>')
def eliminar(id):
    cur = mysql.connection.cursor()
    cur.execute(' DELETE FROM productos WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash(f'SE HA ELIMINADO CON EXITO EL PRODUCTO  DE LA LISTA ')
    return redirect(url_for('index') )




if __name__ == '__main__':
    lista.run(port = 3000, debug = True)