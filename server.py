import os

from flask import Flask
from flask import Blueprint, render_template
from handlers import site

def create_app():
    app = Flask(__name__)
    app.register_blueprint(site)
    return app


def main():
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True
    app = create_app()
    app.run(host='0.0.0.0', port=port, debug=True)

if __name__ == '__main__':
    main()
