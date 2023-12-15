'''Alerts Module'''
import json
import os
import sys
from multiprocessing.pool import ThreadPool

import requests

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')
from pyng import db, scheduler, app, config
from pyng.database import Hosts, HostAlerts
from pyng.api import get_alerts_enabled


def update_host_status_alert_schedule(alert_interval):
    '''Updates the PHost Status Change Alert schedula via APScheduler'''
    # Attempt to remove the current scheduler
    try:
        scheduler.remove_job('Alerta de cambio de estado del host')
    except Exception:
        pass

    scheduler.add_job(id='Alerta de cambio de estado del host', func=_host_status_alerts_threaded, trigger='interval',
                      seconds=int(alert_interval), max_instances=1)


def _host_status_alerts_threaded():
    with app.app_context():
        alerts_enabled = json.loads(get_alerts_enabled())['alerts_enabled']
       # smtp_configured = json.loads(get_smtp_configured())['smtp_configured']
        alerts = HostAlerts.query.filter_by(alert_cleared=False).all()

        for alert in alerts:
            alert.alert_cleared = True

        if alerts_enabled:
            pool = ThreadPool(config['Max_Threads'])
            threads = []

            message = ''
            for alert in alerts:
                threads.append(
                    pool.apply_async(_get_alert_status_message, (alert,))
                )

            pool.close()
            pool.join()

            for thread in threads:
                message += thread.get()

           # if message:
            #    recipients = ';'.join(
             #       x['email'] for x in Schemas.users(many=True).dump(Users.query.filter_by(alerts_enabled=True)))

              #  try:
               #     send_smtp_message(
                #        recipient=recipients,
                 #       subject='PYNG - Host en estado de alerta',
                  #      message=message
                   # )

                #except Exception as exc:
                 #   log.error('No se pudo enviar el correo electrónico de alerta de cambio de estado del host: {}'.format(exc))

        db.session.commit()


def _get_alert_status_message(alert):
    with app.app_context():
        host = Hosts.query.filter_by(id=alert.host_id).first()
        message = 'El host {}  [IP: {}]: cambio su estado a {} a las  {}'.format(
            host.hostname,
            host.ip_address,
            host.status,
            host.last_poll
        )
        r = requests.post(
            'https://api.telegram.org/bot2146283003:AAEToMafEXoZ-cjtPH8DNyODxVFVPg2xUN8/sendMessage',
            data={'chat_id': '1584727635', 'text': message})
        data = json.loads(r.text)

        return message

