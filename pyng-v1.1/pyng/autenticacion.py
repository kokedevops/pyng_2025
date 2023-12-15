'''User Auth Library'''
import os
import sys

import flask_login
from flask import Blueprint, render_template, redirect, url_for, request, flash
from passlib.hash import sha256_crypt
from password_strength import PasswordPolicy

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')
from pyng import login_manager, db, config, log
from pyng.database import Users
from pyng.schemas import Schemas
from pyng.forms import LoginForm, UpdatePasswordForm, UpdateEmailForm
from pyng.main import database_configured

auth = Blueprint('auth', __name__)


##########################
# Routes #################
##########################
@auth.route("/logout")
@flask_login.login_required
def logout():
    '''Logout user'''
    flask_login.logout_user()
    # return redirect(request.referrer)
    return redirect(url_for('main.index'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    '''Login page'''
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            remember_me = form.remember_me.data

            if not get_user(username) or not verify_password(username, password):
                flash('Combinacion Usuario/Clave Incorrecta', 'danger')
                return redirect(url_for('auth.login'))

            user = User()
            user.id = username
            flask_login.login_user(user, remember=remember_me)
            return redirect(url_for('main.index'))
        else:
            for dummy, errors in form.errors.items():
                for error in errors:
                    flash(error, 'danger')

        return redirect(url_for('auth.login'))


@auth.route('/updatePassword', methods=['POST'])
@flask_login.login_required
def update_password():
    form = UpdatePasswordForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if not verify_password(flask_login.current_user.id, form.current_password.data):
                flash('La contraseña actual no es válida', 'danger')
                return redirect(url_for('main.account'))
            if not form.new_password.data == form.verify_password.data:
                flash('Las contraseñas no coinciden', 'danger')
                return redirect(url_for('main.account'))
            if test_password(form.new_password.data):
                reqs = form.new_password.description
                flash('La contraseña no se cumplió {}'.format(reqs), 'danger')
                return redirect(url_for('main.account'))

            try:
                current_user = Users.query.filter_by(username=flask_login.current_user.id).first()
                current_user.password = sha256_crypt.hash(form.new_password.data)
                db.session.commit()
                flash('Contraseña actualizada correctamente', 'success')
            except Exception as exc:
                log.error('No se pudo actualizar la contraseña del usuario.: {}'.format(exc))
                flash('No se pudo actualizar la contraseña', 'danger')

        else:
            for dummy, errors in form.errors.items():
                for error in errors:
                    flash(error, 'danger')

        return redirect(url_for('main.account'))


@auth.route('/updateEmail', methods=['POST'])
@flask_login.login_required
def update_email():
    form = UpdateEmailForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if not verify_password(flask_login.current_user.id, form.password.data):
                flash('La contraseña actual no es válida', 'danger')
                return redirect(url_for('main.account'))
            if not form.email.data == form.email_verify.data:
                flash('Las direcciones de correo electrónico no coinciden', 'danger')
                return redirect(url_for('main.account'))

            try:
                current_user = Users.query.filter_by(username=flask_login.current_user.id).first()
                current_user.email = form.email.data
                db.session.commit()
                flash('Correo electrónico actualizado correctamente', 'success')
            except Exception as exc:
                log.error('No se pudo actualizar la dirección de correo electrónico.: {}'.format(exc))
                flash('No se pudo actualizar la dirección de correo electrónico.', 'danger')

        else:
            for dummy, errors in form.errors.items():
                for error in errors:
                    flash(error, 'danger')

        return redirect(url_for('main.account'))


@auth.route('/addUser', methods=['GET', 'POST'])
@flask_login.login_required
def add_user():
    '''Add user to database'''
    if request.method == 'GET':
        return render_template('addUser.html')
    elif request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        password_verify = request.form.get('verify_password')
        errors = 0

        if password != password_verify:
            # Verify passwords matched
            flash('Las contraseñas no coinciden', 'danger')
            errors += 1
        if Users.query.filter_by(username=username).first():
            # Check to see if username exists
            flash('Usuario ya existe', 'danger')
            errors += 1
        if Users.query.filter_by(email=email).first():
            # Check to see if email already exists
            flash('Email ya existe', 'danger')
            errors += 1

        if errors:
            return redirect(url_for('auth.add_user'))

        try:
            # create new user with the form data. Hash the password so plaintext version isn't saved.
            new_user = Users(email=email, username=username, password=sha256_crypt.hash(password))

            # add the new user to the database
            db.session.add(new_user)
            db.session.commit()
            flash('Usuario agregado exitosamente {}'.format(new_user.username), 'success')
        except Exception:
            flash('No se pudo agregar al usuario', 'danger')

        return redirect(url_for('auth.add_user'))


##########################
# Login Manager ##########
##########################
class User(flask_login.UserMixin):
    '''User object'''


@login_manager.user_loader
def user_loader(username):
    '''Load user'''
    if not get_user(username):
        return

    user = User()
    user.id = username
    user.email = get_user(username)['email']
    return user


@login_manager.request_loader
def request_loader(req):
    '''Login request'''
    username = req.form.get('username')
    password = req.form.get('password')

    if not get_user(username):
        # Username not found
        return

    if not verify_password(username, password):
        # Invalid password provided
        return

    user = User()
    user.id = username

    return user


##########################
# Functions ##############
##########################
def get_user(username):
    """Get user based on username

    Args:
        username (str): Username

    Returns:
        dict
    """
    if database_configured():
        user_data = Users.query.filter_by(username=username).first()
        return Schemas.users(many=False).dump(user_data)
    else:
        return None


def verify_password(username, password):
    """Verify password entered using SHA256 Encryption.

    Args:
        form (dict): A dictionary of form info

    Returns:
        bool: Whether or not the password was verified.
    """
    return sha256_crypt.verify(password, get_user(username)['password'])


def test_password(password):
    """Verify a password meets our defined password policy

    Args:
        password (str): Password to test

    Returns:
        list: A list containing which tests have failed
    """
    policy = PasswordPolicy.from_names(
        length=config['Password_Policy']['Length'],
        uppercase=config['Password_Policy']['Uppercase'],
        nonletters=config['Password_Policy']['Nonletters']
    )
    return policy.test(password)
