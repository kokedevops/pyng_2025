'''SMTP Library'''
import json
import os
import smtplib
import sys
from email.mime.text import MIMEText

import flask_login
from flask import Blueprint, render_template, redirect, url_for, request, flash

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')
from pyng import db, log
from pyng.database import SmtpServer
from pyng.api import get_smtp_configured, get_smtp_config
from pyng.forms import SmtpConfigForm

smtp = Blueprint('smtp', __name__)


##########################
# Routes #################
##########################
@smtp.route("/configureSMTP", methods=['GET', 'POST', 'DELETE'])
@flask_login.login_required
def configure_smtp():
    '''SMTP Config'''
    form = SmtpConfigForm()
    if request.method == 'GET':
        return render_template('smtpConfig.html', smtp=json.loads(get_smtp_config()), form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            try:
                smtp_conf = SmtpServer.query.first()
                smtp_conf.smtp_server = form.server.data
                smtp_conf.smtp_port = form.port.data
                smtp_conf.smtp_sender = form.sender.data
                db.session.commit()
                flash('Configuracion SMTP actualizada correctamente', 'success')
            except Exception as exc:
                flash('Configuracion SMTP fallida: {}'.format(exc), 'danger')
        else:
            for dummy, errors in form.errors.items():
                for error in errors:
                    flash(error, 'danger')
    elif request.method == 'DELETE':
        try:
            smtp_conf = SmtpServer.query.first()
            smtp_conf.smtp_server = ''
            smtp_conf.smtp_port = ''
            smtp_conf.smtp_sender = ''
            db.session.commit()
            flash('Successfully removed SMTP configuration', 'success')
        except Exception:
            flash('Failed to remove SMTP configuration', 'danger')

    return redirect(url_for('smtp.configure_smtp'))


@smtp.route("/smtpTest", methods=['POST'])
@flask_login.login_required
def smtp_test():
    '''Send SMTP test email'''
    if request.method == 'POST':
        results = request.form.to_dict()
        subject = 'PYNG SMTP PRUEBA'
        message = 'MENSAJE DE PRUEBA PYNG'

        try:
            send_smtp_message(results['recipient'], subject, message)
            flash('Successfully sent SMTP test message', 'success')
        except Exception as exc:
            flash('Failed to send SMTP test message: {}'.format(exc), 'danger')

    return redirect(url_for('smtp.configure_smtp'))


##########################
# Functions ##############
##########################
def send_smtp_message(recipient, subject, message):
    '''Send SMTP message'''
    current_smtp = json.loads(get_smtp_config())

    if not json.loads(get_smtp_configured())['smtp_configured']:
        log.error('Intentando enviar un mensaje SMTP pero SMTP no esta configurado.')
        return

    msg = MIMEText(message, 'html')
    msg['Subject'] = subject
    msg['From'] = current_smtp['smtp_sender']

    try:
        server = smtplib.SMTP(current_smtp['smtp_server'], current_smtp['smtp_port'], timeout=10)
    except Exception as exc:
        log.error('No se pudo iniciar el servidor SMTP: {}'.format(exc))
        raise exc

    # Secure the connection
    server.starttls()

    # Send ehlo
    server.ehlo()
    server.set_debuglevel(False)

    # Send message
    server.sendmail(current_smtp['smtp_sender'], recipient, msg.as_string())
    server.quit()
