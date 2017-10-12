from flask import Blueprint, render_template


site = Blueprint('site', __name__)


@site.route('/')
def home_page():
    return render_template('home/index.html')

@site.route('/restaurant')
def restaurant_home_page():
    return render_template('restaurant/index.html')

@site.route('/restaurant/12') #Change me with model [ID]
def restaurant_show_page():
    return render_template('restaurant/show.html')

@site.route('/restaurant/12/edit')
def restaurant_edit_page():
    return render_template('restaurant/edit.html')

@site.route('/user/12/restaurant/new')
def restaurant_new_page():
    return render_template('restaurant/new.html')


@site.route('/register')
def register_home_page():
    return render_template('register/index.html')
