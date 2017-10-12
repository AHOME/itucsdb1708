import datetime
import os

from flask import Flask
from flask import render_template


app = Flask(__name__)

@app.route('/')
def home_page():
    now = datetime.datetime.now()
    return render_template('home/index.html', current_time=now.ctime())

@app.route('/restaurant')
def restaurant_home_page():
    now = datetime.datetime.now()
    return render_template('restaurant/index.html', current_time=now.ctime())

@app.route('/restaurant/12') #Change me with model [ID]
def restaurant_show_page():
    now = datetime.datetime.now()
    return render_template('restaurant/show.html', current_time=now.ctime())


if __name__ == '__main__':
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True
    app.run(host='0.0.0.0', port=port, debug=debug)
