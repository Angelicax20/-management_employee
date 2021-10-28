from re import U
from flask import Flask, render_template, redirect, session, flash, request
from markupsafe import escape
from werkzeug.security import check_password_hash, generate_password_hash
from db import seleccion, accion
#from dbmysql import seleccion2, accion2
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
    if userlog.strip()=="":
        return redirect('/login')
    elif session['tipoUsuario'] == 'empleado':
        return redirect('/empleado')
    else:
       return render_template('index.html')

@app.route('/logout/', methods=['GET','POST'])
def logout():
    session.clear()
    global userlog
    userlog = ""
    return redirect('/')

@app.route('/crear-usuario/', methods=['GET', 'POST'])
def crear_usuario():
        global userlog
        global accionGlobal
        global idUsuario
        if userlog.strip()=="":
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
                titulo = 'Registro de datos'
                if request.args.get('accion') == 'edicionUsuario':
                    accionGlobal = 'editarUsuario'
                else:
                    accionGlobal = 'CrearUsuario'

                if accionGlobal == 'editarUsuario':
                    
                    idUsuario = request.args.get('idUsuario')
                    
                    sql = f"SELECT * FROM Usuario WHERE docIdentidad = '{idUsuario}';"
                    try:
                        resultadoUpdate = seleccion(sql)
                    except:
                        #resultadoUpdate = seleccion2(sql)
                        pass    

                    parametrosURL['datosUsuario'] = resultadoUpdate
                    parametrosURL['accion'] = 'editar'
                    titulo='Edición de usuario'
                    
                return render_template('crear-usuario.html', prueba=frm, titulo=titulo, parametros = parametrosURL)

            else:
                titulo = 'Registro de datos'
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
                    try:
                           
                        res = accion(sql, (numeroDocumento, nombres, apellidos, fechaNacimiento, telefono, email, tipoContrato, salario, fechaTerminoContrato, clave, tipoDoc, fechaIngreso, cargo, tipoUsuario, 'A'))
                    except:
                       #res = accion2(sql, (numeroDocumento, nombres, apellidos, fechaNacimiento, telefono, email, tipoContrato, salario, fechaTerminoContrato, clave, tipoDoc, fechaIngreso, cargo, tipoUsuario, 'A'))
                        pass
                    # Proceso los resultados
                    # linea de prueba    
                    # print(res)

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
                    try:
                        res = accion(sql, (numeroDocumento, nombres, apellidos, fechaNacimiento, telefono, email, tipoContrato, fechaTerminoContrato, salario, clave, tipoDoc, fechaIngreso, cargo, tipoUsuario, idUsuario))
                    except:
                        #res = accion2(sql, (numeroDocumento, nombres, apellidos, fechaNacimiento, telefono, email, tipoContrato, fechaTerminoContrato, salario, clave, tipoDoc, fechaIngreso, cargo, tipoUsuario, idUsuario))
                        pass
                    # linea de prueba 
                    #print("idUsuario vale:")
                    #print(idUsuario)

                    if res == 0:
                        parametrosURL['proceso'] = "actualizado error"
                        parametrosURL['icon'] = "error"
                        parametrosURL['descripcion'] = "Intente actualizar con otro numero de documento"
                    else:
                        parametrosURL['proceso'] = "actualizado ok"
                        parametrosURL['icon'] = "success"
                        parametrosURL['descripcion'] = "Actualización exitosa"

                        idUsuario = ''
                    
                    titulo = 'Edición de usuario'


                return render_template('crear-usuario.html', prueba=frm, titulo='Registro de datos', parametros = parametrosURL)

@app.route('/gestionar-usuario/', methods=['GET', 'POST'])
def gestionar():
    global userlog
    if userlog.strip()=="":
        return redirect('/login')
    elif session['tipoUsuario'] == 'empleado':
        return redirect('/empleado')
    else:
        parametrosURL = {
            'estadoUpdate' : 'noUpdate'
        }

        if request.method == 'GET':


            if request.args.get('accion') == 'eliminarUsuario':
                idUsuario = request.args.get('idUsuario')


                sqlUpdate = "UPDATE Usuario SET estado = ? WHERE docIdentidad = ?"
                try:
                    res = accion(sqlUpdate, ('I',idUsuario))
                except:
                    #res = accion2(sqlUpdate, ('I',idUsuario))
                    pass
                if res == 0:
                    parametrosURL['estadoUpdate'] = 'delete error'
                else:
                    parametrosURL['estadoUpdate'] = 'delete succes'

            if request.args.get('accion') == 'generarReporte':
                sql = "INSERT INTO Reporte (descripcion, puntaje, Usuario_idDocumento_FK) VALUES (?,?,?);"

                idUsuario = request.args.get('idUsuario')
                puntaje = request.args.get('puntaje')
                descripcion = request.args.get('descripcion')
                try:
                    res = accion(sql, (descripcion, puntaje, idUsuario))
                except:
                    #res = accion2(sql, (descripcion, puntaje, idUsuario))
                    pass

                if res == 0:
                    parametrosURL['estadoUpdate'] = 'insert report error'
                else:
                    parametrosURL['estadoUpdate'] = 'insert report succes'


            sql = f"SELECT * FROM Usuario WHERE estado = 'A';"
            try:
                resultado = seleccion(sql)
            except:    
                #resultado = seleccion2(sql)
                pass
        return render_template('gestionar-usuario.html', titulo='Gestionar usuario', usuarios=resultado, parametros = parametrosURL)

@app.route('/empleado/', methods=['GET', 'POST'])
def empleado():
    global userlog
    if userlog.strip()=="":
        return redirect('/login')
        
    elif session['tipoUsuario'] == 'empleado':

        if request.method == 'GET':
            datosEmpleado = session['datosEmpleado']

            idDocumento = datosEmpleado[0][0]
            sql = f"SELECT max(idReporte), descripcion, puntaje, Usuario_idDocumento_FK  FROM Reporte WHERE Usuario_idDocumento_FK = {idDocumento}"
            try:    
                res = seleccion(sql)
            except:
                #res = seleccion2(sql)
                pass

            return render_template('empleado.html', titulo='Empleado', datosSesion = datosEmpleado, infoReporte = res)
    elif session['tipoUsuario'] == 'admin':
         return redirect('/')
    else:
        # linea de prueba 
        #print(session['tipoUsuario'])
        return redirect('/login')

@app.route('/login/',methods=['GET', 'POST'])
def login():
    empleado
    try :
        if session['tipoUsuario'] == 'empleado':
            return redirect('/empleado/')
        else:
            return redirect('/home')  
    except:
        pass

      
    global userlog
    userlog = ""
    
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
        try:
            res = seleccion(sql)
            #print(res)
        except:
            #res = seleccion2(sql)
            pass

        if len(res) == 0:
            parametrosURL['estadoLogin'] = 'usuario no encontrado'
            return render_template('login.html', prueba=frm_login, parametros=parametrosURL)

        else:
            
            claveBd = res[0][9]

            if check_password_hash(claveBd,password):
                session.clear()
                
                session['tipoUsuario'] = res[0][13]
                session['estado'] = res[0][14]

                if  session['estado'] =='I':
                    session.clear()
                    parametrosURL['estadoLogin'] = 'usuario no encontrado'
                    return render_template('login.html', prueba=frm_login, parametros=parametrosURL)


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

