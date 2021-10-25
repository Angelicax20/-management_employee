from re import U
from flask import Flask, render_template, redirect, session, flash, request
from markupsafe import escape
from werkzeug.security import check_password_hash, generate_password_hash
from db import seleccion, accion
from forms import Registro, Login as lg
import os

app = Flask(__name__)

app.secret_key = os.urandom(24)
userlog = ""
accionGlobal = ''
idUsuario = ''

@app.route('/',methods=['GET', 'POST'])
@app.route('/index/',methods=['GET', 'POST'])
@app.route('/home/',methods=['GET', 'POST'])
def home():
    global userlog
    print(userlog)
    if userlog=="":
        print(userlog)
        return redirect('/login')
        
    else:
        print(userlog)
        return render_template('index.html')

@app.route('/logout/', methods=['GET','POST'])
def logout():
    session.clear()
    global userlog
    print(userlog)
    userlog = ""
    print(userlog)
    return redirect('/')

@app.route('/crear-usuario/', methods=['GET', 'POST'])
def crear_usuario():
        global userlog
        global accionGlobal
        global idUsuario
        print(userlog)
        if userlog=="":
            print(userlog)
            return redirect('/login')
        elif session['tipoUsuario'] == 'empleado':
            return redirect('/empleado')
        else:
    

            """ V5. Utiliza almacenamiento seguro para los datos """
            frm = Registro()
            parametrosURL = {
                'typeForm' : "Crear usuario",
                'urlAction' : "/crear-usuario/",
                'proceso' : '',
                'accion' : 'crear'
            }

            if request.method == 'GET':

                if request.args.get('accion') == 'edicionUsuario':
                    accionGlobal = 'editarUsuario'
                else:
                    accionGlobal = 'CrearUsuario'

                if accionGlobal == 'editarUsuario':
                    
                    idUsuario = request.args.get('idUsuario')
                    
                    sql = f"SELECT * FROM Usuario WHERE docIdentidad = '{idUsuario}';"
                    resultadoUpdate = seleccion(sql)


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
                
                if accionGlobal == 'CrearUsuario':
                    sql = "INSERT INTO Usuario (docIdentidad, nombre, apellidos, fechaNac, telefono, correo, tipoContrato, salario, fechaTerContrato, clave, tipoDocumento, fechaIngreso, cargo, tipoUsuario, estado) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"
                    # Ejecutar la consulta
                    clave = generate_password_hash(clave)

                    res = accion(sql, (numeroDocumento, nombres, apellidos, fechaNacimiento, telefono, email, tipoContrato, salario, fechaTerminoContrato, clave, tipoDoc, fechaIngreso, cargo, tipoUsuario, 'A'))
                    # Proceso los resultados

                    print(res)

                    if res == 0:
                        parametrosURL['proceso'] = "insertado error"
                        parametrosURL['icon'] = "error"
                        parametrosURL['descripcion'] = "Intente insertar con otro numero de documento"
                    else:
                        parametrosURL['proceso'] = "insertado ok"
                        parametrosURL['icon'] = "success"
                        parametrosURL['descripcion'] = "Registro exitoso"

                elif accionGlobal == 'editarUsuario': 

                    sql = "UPDATE Usuario SET docIdentidad = ?, nombre = ?, apellidos = ?, fechaNac = ?, telefono = ?, correo = ?, tipoContrato = ?, fechaTerContrato = ?, salario = ?,  clave = ?, tipoDocumento = ?, fechaIngreso = ?, cargo = ?, tipoUsuario = ? WHERE docIdentidad = ?"
                    
                    clave = generate_password_hash(clave)

                    res = accion(sql, (numeroDocumento, nombres, apellidos, fechaNacimiento, telefono, email, tipoContrato, fechaTerminoContrato, salario, clave, tipoDoc, fechaIngreso, cargo, tipoUsuario, idUsuario))

                    print("idUsuario vale:")
                    print(idUsuario)

                    if res == 0:
                        parametrosURL['proceso'] = "actualizado error"
                        parametrosURL['icon'] = "error"
                        parametrosURL['descripcion'] = "Intente actualizar con otro numero de documento"
                    else:
                        parametrosURL['proceso'] = "actualizado ok"
                        parametrosURL['icon'] = "success"
                        parametrosURL['descripcion'] = "Actualización exitosa"

                        idUsuario = ''


                return render_template('crear-usuario.html', prueba=frm, titulo='Registro de datos', parametros = parametrosURL)

@app.route('/gestionar-usuario/', methods=['GET', 'POST'])
def gestionar():
    global userlog
    print(userlog)
    if userlog=="":
        print(userlog)
        return redirect('/login')
    elif session['tipoUsuario'] == 'empleado':
        return redirect('/empleado')
    else:
        print(userlog)
        

        parametrosURL = {
            'estadoUpdate' : 'noUpdate'
        }

        if request.method == 'GET':


            if request.args.get('accion') == 'eliminarUsuario':
                idUsuario = request.args.get('idUsuario')


                sqlUpdate = "UPDATE Usuario SET estado = ? WHERE docIdentidad = ?"
                res = accion(sqlUpdate, ('I',idUsuario))
                
                if res == 0:
                    parametrosURL['estadoUpdate'] = 'delete error'
                else:
                    parametrosURL['estadoUpdate'] = 'delete succes'

            if request.args.get('accion') == 'generarReporte':
                sql = "INSERT INTO Reporte (descripcion, puntaje, Usuario_idDocumento_FK) VALUES (?,?,?);"

                idUsuario = request.args.get('idUsuario')
                puntaje = request.args.get('puntaje')
                descripcion = request.args.get('descripcion')

                res = accion(sql, (descripcion, puntaje, idUsuario))

                if res == 0:
                    parametrosURL['estadoUpdate'] = 'insert report error'
                else:
                    parametrosURL['estadoUpdate'] = 'insert report succes'


            sql = f"SELECT * FROM Usuario WHERE estado = 'A';"
            resultado = seleccion(sql)

        return render_template('gestionar-usuario.html', titulo='Gestionar usuario', usuarios=resultado, parametros = parametrosURL)

@app.route('/empleado/', methods=['GET', 'POST'])
def empleado():
    global userlog
    print(userlog)
    if userlog=="":
        print("entre")
        return redirect('/login')
        
    elif session['tipoUsuario'] == 'empleado':

        print(userlog)    
        if request.method == 'GET':
            datosEmpleado = session['datosEmpleado']

            idDocumento = datosEmpleado[0][0]
            sql = f"SELECT max(idReporte), descripcion, puntaje, Usuario_idDocumento_FK  FROM Reporte WHERE Usuario_idDocumento_FK = {idDocumento}"
            res = seleccion(sql)

            return render_template('empleado.html', titulo='Empleado', datosSesion = datosEmpleado, infoReporte = res)
    elif session['tipoUsuario'] == 'admin':
         return redirect('/')
    else:
        print(session['tipoUsuario'])
        return redirect('/login')

@app.route('/login/',methods=['GET', 'POST'])
def login():
    global userlog
    session.clear()
    print(userlog)
    userlog = ""
    print(userlog)

    parametrosURL = {
        'estadoLogin' : ''
    }
    
    frm_login = lg()

    if request.method == 'GET':
        return render_template('login.html',prueba=frm_login, parametros = parametrosURL)

    else:

        userlog = escape(request.form["usu"]) #cedula
        password = escape(request.form["cla"])

        sql = f"SELECT *  FROM Usuario WHERE docIdentidad='{userlog}'"
        res = seleccion(sql)

        if len(res) == 0:
            parametrosURL['estadoLogin'] = 'usuario no encontrado'
            return render_template('login.html', prueba=frm_login, parametros=parametrosURL)

        else:
            
            claveBd = res[0][9]

            if check_password_hash(claveBd,password):
                session.clear()
                
                session['tipoUsuario'] = res[0][13]

                if session['tipoUsuario'] == 'empleado':
                    session['datosEmpleado'] = res
                    return redirect('/empleado/')

                else:
                    
                    session['idUsuario'] = res[0][0]
                    session['nombreUsuario'] = res[0][1]+" "+res[0][2]
                    return redirect('/index/')
            else:
                parametrosURL['estadoLogin'] = 'clave incorrecta'
                return render_template('login.html', prueba=frm_login, parametros=parametrosURL)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)
if __name__ == '__main__':
    app.run(debug=True)

