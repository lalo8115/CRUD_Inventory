from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "clave_secreta"  # Necesaria para mostrar mensajes flash


# Configura la conexión a la base de datos
def get_db_connection():
    return mysql.connector.connect(
    host="localhost",
    user="root",
    password="380202lin",
    database="flask_db"
)

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # Para devolver resultados como diccionarios
    cursor.execute("SELECT * FROM producto")
    productos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('lista.html', productos=productos)

@app.route('/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        stock = request.form['stock']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO producto (nombre, descripcion, precio, stock) VALUES (%s, %s, %s, %s)",
            (nombre, descripcion, precio, stock)
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash("Producto creado exitosamente!")
        return redirect(url_for('index'))

    return render_template('formulario.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        stock = request.form['stock']

        cursor.execute(
            "UPDATE producto SET nombre = %s, descripcion = %s, precio = %s, stock = %s WHERE id = %s",
            (nombre, descripcion, precio, stock, id)
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash("Producto actualizado exitosamente!")
        return redirect(url_for('index'))

    cursor.execute("SELECT * FROM producto WHERE id = %s", (id,))
    producto = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template('formulario.html', producto=producto)


@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_producto(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM producto WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()

    flash("Producto eliminado exitosamente!")
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
