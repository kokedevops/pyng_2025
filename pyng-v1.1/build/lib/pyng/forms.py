'''Web Forms'''
import os
import sys

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, NumberRange

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')
from pyng import config


class FirstTimeSetupForm(FlaskForm):
    password_policy = 'Politica de contraseña: Longitud mínima ({}), Mínimo de mayúsculas ({}), Mínimo de caracteres especiales ({}).'.format(
        config['Password_Policy']['Length'],
        config['Password_Policy']['Uppercase'],
        config['Password_Policy']['Nonletters']
    )
    username = StringField('Usuario', validators=[DataRequired(message="Usuario requerido")])
    email = StringField('Email', validators=[DataRequired(message="Direccion Email requerida"),
                                             Email(message="Direccion email invalida")])
    password = PasswordField('Clave', description=password_policy,
                             validators=[DataRequired(message="Nueva contraseña requerida")])
    verify_password = PasswordField('Verificar clave',
                                    validators=[DataRequired(message="Verificacion de contraseña requerida")])
    poll_interval = IntegerField('Intervalo de revision (segundos)',
                                 validators=[DataRequired(message="Intervalo de revision requerida")])
    retention_days = IntegerField('Tiempo de retencion de historial (dias)',
                                  validators=[DataRequired(message="Tiempo de retencion de historial requerida")])
    enable_smtp = BooleanField('Activar Alertas por SMTP')
    smtp_server = StringField('Servidor')
    smtp_port = StringField('Puerto')
    smtp_sender = StringField('Direccion de envio')
    submit = SubmitField('Enviar')


class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(message="Usuario requerido")])
    password = PasswordField('Clave', validators=[DataRequired(message="Contraseña requerida")])
    remember_me = BooleanField('Recuerdame')
    submit = SubmitField('Acceder')


class UpdatePasswordForm(FlaskForm):
    desc = 'Politica de contraseña: Longitud mínima ({}), Minimo de mayuscula ({}), Minimo de caracteres especiales ({}).'.format(
        config['Password_Policy']['Length'],
        config['Password_Policy']['Uppercase'],
        config['Password_Policy']['Nonletters']
    )
    current_password = PasswordField('Contraseña actual', validators=[DataRequired(message="Se requiere contraseña actual")])
    new_password = PasswordField('Nueva contraseña', description=desc,
                                 validators=[DataRequired(message="Nueva contraseña requerida")])
    verify_password = PasswordField('Verificar contraseña',
                                    validators=[DataRequired(message="Se requiere verificación de contraseña")])
    submit = SubmitField('Enviar')


class UpdateEmailForm(FlaskForm):
    email = StringField('Nueva dirección de correo electrónico', validators=[DataRequired(message="Dirección de correo electrónico obligatorio"),
                                                         Email(message="Dirección de correo electrónico inválida")])
    email_verify = StringField('Confirme su dirección de correo electrónico',
                               validators=[DataRequired(message="Verificar dirección de correo electrónico requerida"),
                                           Email(message="Dirección de correo electrónico inválida")])
    password = PasswordField('Contraseña', validators=[DataRequired(message="Se requiere contraseña")])
    submit = SubmitField('Enviar')


class SmtpConfigForm(FlaskForm):
    server = StringField('Servidor', validators=[DataRequired(message="Servidor requerido")])
    port = IntegerField('Puerto', validators=[DataRequired(message="Puerto requerido"),
                                            NumberRange(min=0, message="Numero de puerto invalido")])
    sender = StringField('Dirección del remitente', validators=[DataRequired(message="Dirección del remitente requerida"),
                                                       Email(message="Direccion email invalida")])
    submit = SubmitField('Actualizar')


class AddHostsForm(FlaskForm):
    ip_address = TextAreaField('Direccion IP', validators=[DataRequired(message="Direccion IP requerida")])
    submit = SubmitField('Agregar')


class SelectThemeForm(FlaskForm):
    theme = SelectField('Tema', config['Web_Themes'].items())
    submit = SubmitField('Actualizar')


class PollingConfigForm(FlaskForm):
    interval = StringField('Intervalo de revision')
    retention_days = StringField('Días de retención del historial de monitoreo')
    submit = SubmitField('Actualizar')
