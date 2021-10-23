from flask_wtf import FlaskForm
from wtforms import TextField, SubmitField, PasswordField, DateField, IntegerField, SelectField, DecimalField
from wtforms.fields.html5 import EmailField, DateField, IntegerField, TelField, DecimalField
from wtforms.validators import EqualTo, InputRequired

class Login(FlaskForm):
    usu = TextField('Usuario', validators = [InputRequired(message='Indique el usuario')])
    cla = PasswordField('Contraseña', validators = [InputRequired(message='Indique la clave')])
    btn = SubmitField('Ingresar')

class Registro(FlaskForm):
    nombres = TextField('Nombres', validators = [InputRequired(message='Ingrese un nombre')])

    apellidos = TextField('Apellidos', validators = [InputRequired(message='Ingrese un apellido')])

    fechaNacimiento = DateField('Fecha de nacimiento', validators = [InputRequired(message='Ingrese una fecha de nacimiento')])

    numeroDocumento = IntegerField('Número de documento', validators = [InputRequired(message='Ingrese un numero de documento')])

    tipoDoc = SelectField(u'Tipo de documento', choices=[('', ''),('1', 'Cedula de ciudadanía'), ('2', 'Tarjeta de identidad'), ('3', 'Pasaporte')], validators = [InputRequired(message='Seleccione un tipo de documento')])

    clave = PasswordField('Contraseña', validators = [InputRequired(message='Ingrese una contraseña')])

    telefono = TelField('Teléfono', validators = [InputRequired(message='Ingrese un teléfono')])

    email = EmailField('Email *', validators = [InputRequired(message='Ingrese un email')])

    salario = DecimalField('Salario', validators = [InputRequired(message='Ingrese un salario')])

    tipoContrato = SelectField(u'Tipo de contrato', choices=[('', ''),('Termino fijo','Termino fijo'),('Termino indefinido','Termino indefinido'), ('Obra o labor','Obra o labor'), ('Aprendizaje','Aprendizaje'), ('Temporal ocasional o accidental','Temporal ocasional o accidental'), ('Prestación de servicios','Prestación de servicios')], validators = [InputRequired(message='Seleccione un tipo de contrato')])

    fechaTerminoContrato = DateField('Fecha termino de contrato', validators = [InputRequired(message='Ingrese una fecha de cierre de contrato')])
    
    fechaIngreso = DateField('Fecha termino de ingreso', validators = [InputRequired(message='Ingrese una fecha de ingreso')])

    cargo = TextField('Cargo', validators = [InputRequired(message='Ingrese un cargo')])

    tipoUsuario = SelectField(u'Tipo de usuario', choices=[('', ''),('admin', 'Administrador'), ('empleado', 'Empleado')], validators = [InputRequired(message='Seleccione el tipo de usuario')])

    btnEnviar = SubmitField('Crear usuario')

