from flask import Flask, render_template
from flask_migrate import Migrate
from config import Config
from extensions import db
from models import *

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/equipment')
def equipment():
    return render_template('equipment.html')

@app.route('/request')
def request_form():
    return render_template('request_form.html')

@app.route('/kanban')
def kanban():
    return render_template('kanban.html')

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

if __name__ == "__main__":
    app.run(debug=True)
