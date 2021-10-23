
from flask import Flask, render_template, redirect, session, flash, request
from markupsafe import escape
from werkzeug.security import check_password_hash, generate_password_hash
from db import seleccion, accion
from forms import Registro, Login as lg
import os

app = Flask(__name__)

app.secret_key = os.urandom(24)
userlog = ""
@app.route('/',methods=['GET', 'POST'])
@app.route('/index/',methods=['GET', 'POST'])
@app.route('/home/',methods=['GET', 'POST'])
def home():
    global userlog 
    if request.method == 'GET' and  userlog=="":
        return login()
    else:
        if userlog=="":
            userlog=escape(request.form["usu"]) 
        return render_template('index.html',usuario=userlog)



accion = ''

@app.route('/crear-usuario/', methods=['GET', 'POST'])
def crear_usuario():
    global accion

    """ V5. Utiliza almacenamiento seguro para los datos """
    frm = Registro()
    parametrosURL = {
        'typeForm' : "Crear usuario",
        'urlAction' : "/crear-usuario/",
        'proceso' : '',
        'accion' : 'crear'
    }
    
    if request.args.get('accion'):
        accion = 'editarUsuario'
    else:
        accion = 'CrearUsuario'

    if request.method == 'GET':

        if accion == 'editarUsuario':
            idUsuario = request.args.get('idUsuario')
            sql = f"SELECT * FROM Usuario WHERE docIdentidad = '{idUsuario}';"
            resultadoUpdate = seleccion(sql)
            
            print(resultadoUpdate)

            parametrosURL['datosUsuario'] = resultadoUpdate
            parametrosURL['accion'] = 'editar'
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

            if accion == 'CrearUsuario':
                sql = "INSERT INTO Usuario (docIdentidad,nombre,apellidos,fechaNac,telefono,correo,tipoContrato,fechaTerContrato,salario,clave, tipoDocumento, fechaIngreso, cargo, tipoUsuario) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?);"
                # Ejecutar la consulta
                clave = generate_password_hash(clave)

                res = accion(sql, (numeroDocumento, nombres, apellidos, fechaNacimiento, telefono, email, tipoContrato, fechaTerminoContrato, salario, clave, tipoDoc, fechaIngreso, cargo, tipoUsuario))
                # Proceso los resultados

                if res==0:
                    parametrosURL['proceso'] = "insertado error"
                    parametrosURL['icon'] = "error"
                    parametrosURL['descripcion'] = "Intente insertar con otro numero de documento"
                else:
                    parametrosURL['proceso'] = "insertado ok"
                    parametrosURL['icon'] = "success"
                    parametrosURL['descripcion'] = "Registro exitoso"

            elif accion == 'editarUsuario':
                pass

        return render_template('crear-usuario.html', prueba=frm, titulo='Registro de datos', parametros = parametrosURL)

@app.route('/gestionar-usuario/', methods=['GET', 'POST'])
def gestionar():

    if request.method == 'GET':
        sql = f"SELECT * FROM Usuario;"
        resultado = seleccion(sql)

    return render_template('gestionar-usuario.html', titulo='Gestionar usuario', usuarios=resultado)


@app.route('/empleado/')
def empleado():
    return render_template('empleado.html', titulo='Empleado')


@app.route('/login/',methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        frm_login = lg()
        return render_template('login.html',prueba=frm_login)
    else:
        return render_template('index.html')
        # return home();
    


if __name__ == '__main__':
    app.run(debug=True)


