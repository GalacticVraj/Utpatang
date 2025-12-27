from flask import Flask, render_template, request, redirect, url_for
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

@app.route("/equipment", methods=["GET", "POST"])
def equipment():
    if request.method == "POST":
        eq = Equipment(
            name=request.form["name"],
            serial_number=request.form["serial"],
            department=request.form["department"],
            assigned_employee=request.form["employee"],
            maintenance_team=request.form["team"],
            default_technician=request.form["technician"],
            location=request.form["location"]
        )
        db.session.add(eq)
        db.session.commit()
        return redirect("/equipment")

    all_equipment = Equipment.query.all()
    return render_template("equipment.html", equipment=all_equipment)

@app.route("/create_request", methods=["GET", "POST"])
def create_request():
    equipment = Equipment.query.all()

    if request.method == "POST":
        eq = Equipment.query.get(request.form["equipment_id"])

        req = MaintenanceRequest(
            subject=request.form["subject"],
            request_type=request.form["type"],
            equipment_id=eq.id,
            equipment_name=eq.name,
            team=eq.maintenance_team,
            technician=eq.default_technician,
            scheduled_date=None, # Handle date parsing if needed, assumed handled or None for now
        )
        
        # Simple date handling if provided
        if request.form.get("scheduled_date"):
            # assuming format YYYY-MM-DD from HTML date input
            from datetime import datetime
            date_str = request.form.get("scheduled_date")
            try:
                req.scheduled_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                pass # or handle error

        db.session.add(req)
        db.session.commit()
        return redirect("/kanban")

    return render_template("request_form.html", equipment=equipment)

@app.route('/kanban')
def kanban():
    return render_template('kanban.html')

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

if __name__ == "__main__":
    app.run(debug=True)
