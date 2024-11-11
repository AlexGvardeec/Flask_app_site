from flask import Blueprint, render_template, abort

about_us = Blueprint('about_us', __name__)


@about_us.route('/about_us/')
def about_us_page():
    return render_template('about_us/about_us.html',
                           title='О нас')
