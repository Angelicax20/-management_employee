
from flask import Flask, render_template, redirect, session, flash, request
from markupsafe import escape
from werkzeug.security import check_password_hash, generate_password_hash
from db import seleccion, accion
from forms import Registro , Login as lg
import os

app = Flask(__name__)

app.secret_key = os.urandom(24)

@app.route('/')
@app.route('/index/')
@app.route('/home/')
def home():
    return render_template('index.html')





@app.route('/crear-usuario/', methods=['GET', 'POST'])
def crear_usuario():

    """ V5. Utiliza almacenamiento seguro para los datos """
    frm = Registro()
    parametrosURL = {
        'typeForm' : "Crear usuario",
        'urlAction' : "/crear-usuario/",
        'proceso' : ''
    }

    if request.method == 'GET':
        return render_template('crear-usuario.html', prueba=frm, titulo='Registro de datos', parametros = parametrosURL)
    else:
        
        nombres = escape(request.form['nombres'])
        apellidos = escape(request.form['apellidos'])
        fechaNacimiento = escape(request.form['fechaNacimiento'])
        numeroDocumento = escape(request.form['numeroDocumento'])
        tipoDoc = escape(request.form['tipoDoc'])
        clave = escape(request.form['clave'])
        telefono = escape(request.form['telefono'])
        email = escape(request.form['email'])
        salario = escape(request.form['salario'])
        tipoContrato = escape(request.form['tipoContrato'])
        fechaTerminoContrato = escape(request.form['fechaTerminoContrato'])
        fechaIngreso = escape(request.form['fechaIngreso'])
        cargo = escape(request.form['cargo'])
        tipoUsuario = escape(request.form['tipoUsuario'])

        swerror = False
        if nombres==None or len(nombres)==0:
            flash('ERROR: Debe suministrar un nombre de usuario')
            swerror = True

        if not swerror:
             # Preparar el query -- Paramétrico

            sql = "INSERT INTO Usuario (docIdentidad,nombre,apellidos,fechaNac,telefono,correo,tipoContrato,fechaTerContrato,salario) VALUES (?,?,?,?,?,?,?,?,?);"
            # Ejecutar la consulta
            clave = generate_password_hash(clave)

            res = accion(sql, (numeroDocumento, nombres, apellidos, fechaNacimiento, telefono, email, tipoContrato, fechaTerminoContrato, salario))
            # Proceso los resultados

            if res==0:
                parametrosURL['proceso'] = "insertado error"
                parametrosURL['icon'] = "error"
                parametrosURL['descripcion'] = "Intente insertar con otro numero de documento"
            else:
                parametrosURL['proceso'] = "insertado ok"
                parametrosURL['icon'] = "success"
                parametrosURL['descripcion'] = "Registro exitoso"

        frm2 = Registro()
        return render_template('crear-usuario.html', prueba=frm2, titulo='Registro de datos', parametros = parametrosURL)

@app.route('/gestionar-usuario/')
def gestionar():
    return render_template('gestionar-usuario.html', titulo='Gestionar usuario')


@app.route('/empleado/')
def empleado():
    return render_template('empleado.html', titulo='Empleado')


@app.route('/login/',methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        frm_login = lg()
        return render_template('login.html',prueba=frm_login)
    else:
        return home();
    


if __name__ == '__main__':
    app.run(debug=True)