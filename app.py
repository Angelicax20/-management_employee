from flask import Flask,render_template

app = Flask(__name__)

@app.route('/')
@app.route('/index/')
@app.route('/home/')

def home():
    return render_template('index.html')


@app.route('/crear-usuario/')
def crear_usuario():
    return render_template('crear-usuario.html',titulo='Crear usuario')


@app.route('/gestionar-usuario/')
def gestionar():
    return render_template('gestionar-usuario.html',titulo='Gestionar usuario')


@app.route('/empleado/')
def empleado():
    return render_template('empleado.html',titulo='Empleado')


@app.route('/login/')
def login():
    return render_template('login.html',titulo='login')

if __name__ == '__main__':
    app.run(debug=True)

