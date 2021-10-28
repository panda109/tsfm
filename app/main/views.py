
from . import main
from flask import render_template

@main.route('/hello')
def publish_hello():
    return render_template('index.html')