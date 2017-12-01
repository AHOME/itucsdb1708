import os
import json
import re

from flask import Flask, session
from flask import Blueprint, render_template
from flask_login import LoginManager,login_user,login_required,current_user
from flask_login import logout_user
from classes.users import *
from handlers import site


login_manager = LoginManager()

@login_manager.user_loader
def load_user( db_mail ):
    return get_user(db_mail)
     

def create_app():
    app = Flask(__name__)
    app.config.from_object('settings')
    app.register_blueprint(site)
    login_manager.init_app(app)
    #login_manager.login_view = 'site.home_page'
    return app


def get_elephantsql_dsn(vcap_services):
    """Returns the data source name for ElephantSQL."""
    parsed = json.loads(vcap_services)
    uri = parsed["elephantsql"][0]["credentials"]["uri"]
    match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
    user, password, host, _, port, dbname = match.groups()
    dsn = """user='{}' password='{}' host='{}' port={}
             dbname='{}'""".format(user, password, host, port, dbname)
    return dsn


def main():
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port,debug = 5000, True

    VCAP_SERVICES = os.getenv('VCAP_SERVICES')
    if VCAP_SERVICES is not None:
        app.config['dsn'] = get_elephantsql_dsn(VCAP_SERVICES)
    else:
        app.config['dsn'] = """user='vagrant' password='vagrant'
                                   host='localhost' port=5432 dbname='itucsdb'"""
    app.run(host='0.0.0.0', port=port, debug=True)

if __name__ == '__main__':
    app = create_app()
    main()
