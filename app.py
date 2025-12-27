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
    # Reports
    from sqlalchemy import func
    team_reports = db.session.query(MaintenanceRequest.team, func.count(MaintenanceRequest.id)).group_by(MaintenanceRequest.team).all()
    dept_reports = db.session.query(Equipment.department, func.count(MaintenanceRequest.id)).join(MaintenanceRequest, Equipment.id == MaintenanceRequest.equipment_id).group_by(Equipment.department).all()
    
    return render_template('dashboard.html', team_reports=team_reports, dept_reports=dept_reports)

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
    # Attach open request counts
    for eq in all_equipment:
        eq.open_requests_count = MaintenanceRequest.query.filter(
            MaintenanceRequest.equipment_id == eq.id,
            MaintenanceRequest.stage.notin_(["Repaired", "Scrap"])
        ).count()
        
    return render_template("equipment.html", equipment=all_equipment)

@app.route("/create_request", methods=["GET", "POST"])
def create_request():
    equipment = Equipment.query.all()
    
    # Pre-fill from query params if available (e.g. from calendar)
    pre_date = request.args.get('date', '')
    pre_type = request.args.get('type', 'Corrective')

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

    return render_template("request_form.html", equipment=equipment, pre_date=pre_date, pre_type=pre_type)

@app.route('/kanban')
def kanban():
    requests = MaintenanceRequest.query.all()
    stages = ["New", "In Progress", "Repaired", "Scrap"]
    return render_template('kanban.html', requests=requests, stages=stages, today=date.today())

@app.route('/api/requests/update', methods=['POST'])
def update_request():
    data = request.json
    req_id = data.get('id')
    new_stage = data.get('stage')
    
    req = MaintenanceRequest.query.get(req_id)
    if not req:
        return {"error": "Request not found"}, 404
    
    req.stage = new_stage
    
    # Scrap Logic: If moved to Scrap, set equipment as scrapped
    if new_stage == "Scrap":
        eq = Equipment.query.get(req.equipment_id)
        if eq:
            eq.is_scrapped = True
            
    # If completed/repaired, we might want to ask for duration, but for now just move it
    # Duration could be sent in the same payload or a separate call
    if 'actual_duration' in data:
        req.actual_duration = data['actual_duration']

    db.session.commit()
    return {"success": True}

@app.route('/equipment/<int:id>/maintenance')
def equipment_maintenance(id):
    eq = Equipment.query.get_or_404(id)
    requests = MaintenanceRequest.query.filter_by(equipment_id=id).all()
    return render_template('equipment_requests.html', equipment=eq, requests=requests)

@app.route('/calendar')
def calendar():
    preventive_requests = MaintenanceRequest.query.filter_by(request_type='Preventive').all()
    # Format for FullCalendar
    events = []
    for req in preventive_requests:
        if req.scheduled_date:
            events.append({
                'title': f"{req.equipment_name}: {req.subject}",
                'start': req.scheduled_date.isoformat(),
                'id': req.id,
                'color': '#28a745'
            })
    return render_template('calendar.html', events=events)

if __name__ == "__main__":
    app.run(debug=True)
