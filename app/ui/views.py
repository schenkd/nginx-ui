from app.ui import ui
from flask import render_template


@ui.route('/',  methods=['GET'])
def index():
    return render_template('index.html')
