from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import re
from config import Config
from extensions import db
from models import *

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def dashboard():
    # Reports
    from sqlalchemy import func
    from datetime import date
    
    # 1. Critical Equipment (Health < 30)
    critical_eq_count = Equipment.query.filter(Equipment.health_score < 30).count()
    
    # 2. Technician Load (Utilization)
    # Assumption: 5 active requests = 100% load
    active_req_count = MaintenanceRequest.query.filter(MaintenanceRequest.stage.notin_(['Repaired', 'Scrap'])).count()
    tech_load = min(int((active_req_count / 5) * 100), 100)
    
    # 3. Open Requests (Pending & Overdue)
    pending_count = MaintenanceRequest.query.filter(MaintenanceRequest.stage.in_(['New', 'In Progress'])).count()
    overdue_count = MaintenanceRequest.query.filter(
        MaintenanceRequest.stage.notin_(['Repaired', 'Scrap']),
        MaintenanceRequest.scheduled_date < date.today()
    ).count()

    team_reports = db.session.query(MaintenanceRequest.team, func.count(MaintenanceRequest.id)).group_by(MaintenanceRequest.team).all()
    
    # Dept reports (Join logic might need adjustment for Work Center requests if they don't have dept)
    # For now, keeping it simple or filtering for requests with equipment_id is not null?
    # Or just use equipment_id join roughly.
    dept_reports = db.session.query(Equipment.department, func.count(MaintenanceRequest.id)).join(MaintenanceRequest, Equipment.id == MaintenanceRequest.equipment_id).group_by(Equipment.department).all()
    
    return render_template('dashboard.html', 
                           team_reports=team_reports, 
                           dept_reports=dept_reports,
                           critical_eq_count=critical_eq_count,
                           tech_load=tech_load,
                           pending_count=pending_count,
                           overdue_count=overdue_count)

@app.route('/work_centers')
@login_required
def list_work_centers():
    work_centers = WorkCenter.query.all()
    return render_template('work_centers.html', work_centers=work_centers)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if not user:
            flash("Account not exist", "danger")
            return redirect(url_for('login'))
            
        if not check_password_hash(user.password_hash, password):
            flash("Invalid Password", "danger")
            return redirect(url_for('login'))
            
        login_user(user)
        return redirect(url_for('dashboard'))
        
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_pass = request.form.get('confirm_password')
        
        if password != confirm_pass:
            flash("Passwords do not match!", "danger")
            return redirect(url_for('signup'))
            
        # Password Validation
        # At least one lowercase, one uppercase, one special char, length > 8
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{9,}$"
        # Note: User said "more then 8 characters", so {9,} or {8,}? usually means >=8. 
        # "length should be in more then 8 charachters" -> > 8 -> 9+
        if len(password) <= 8:
             flash("Password length must be more than 8 characters", "danger")
             return redirect(url_for('signup'))

        if not re.search(r"[a-z]", password):
             flash("Password must contain at least one lowercase letter", "danger")
             return redirect(url_for('signup'))
        if not re.search(r"[A-Z]", password):
             flash("Password must contain at least one uppercase letter", "danger")
             return redirect(url_for('signup'))
        if not re.search(r"[@$!%*?&]", password):
             flash("Password must contain at least one special character (@$!%*?&)", "danger")
             return redirect(url_for('signup'))

        # Check existing user
        if User.query.filter_by(email=email).first():
            flash("Email Id should not be a duplicate in database", "danger")
            return redirect(url_for('signup'))
            
        new_user = User(name=name, email=email, password_hash=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        
        flash("Account Created Successfully! Please Login.", "success")
        return redirect(url_for('login'))
        
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/equipment", methods=["GET", "POST"])
@login_required
def equipment():
    if request.method == "POST":
        eq = Equipment(
            name=request.form["name"],
            serial_number=request.form["serial"],
            department=request.form["department"],
            assigned_employee=request.form["employee"],
            employee_id=request.form.get("employee_id"), # Capture ID
            maintenance_team=request.form["team"],
            default_technician=request.form["technician"],
            location=request.form["location"]
        )
        db.session.add(eq)
        db.session.commit()
        flash("New Equipment Added Successfully!", "success")
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
@login_required
def create_request():
    equipment = Equipment.query.all()
    
    # Pre-fill from query params if available (e.g. from calendar)
    pre_date = request.args.get('date', '')
    pre_type = request.args.get('type', 'Corrective')

    if request.method == "POST":
        maintenance_for = request.form.get("maintenance_for", "Equipment")
        
        req = MaintenanceRequest(
            subject=request.form["subject"],
            request_type=request.form["type"],
            maintenance_for=maintenance_for,
            scheduled_date=None
        )

        if maintenance_for == "Equipment":
            eq = Equipment.query.get(request.form["equipment_id"])
            req.equipment_id = eq.id
            req.equipment_name = eq.name
            req.team = eq.maintenance_team
            req.technician = eq.default_technician
        else:
            wc = WorkCenter.query.get(request.form["work_center_id"])
            req.work_center_id = wc.id
            req.equipment_name = wc.name # Reuse display field
            req.team = "Maintenance" # Default for WC
            req.technician = "Unassigned"
        
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
        flash("Maintenance Request Created Successfully!", "success")
        return redirect("/kanban")

    work_centers = WorkCenter.query.all()
    return render_template("request_form.html", equipment=equipment, work_centers=work_centers, pre_date=pre_date, pre_type=pre_type)

@app.route('/kanban')
@login_required
def kanban():
    requests = MaintenanceRequest.query.all()
    stages = ["New", "In Progress", "Repaired", "Scrap"]
    return render_template('kanban.html', requests=requests, stages=stages, today=date.today())

@app.route('/api/requests/update', methods=['POST'])
@login_required
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
@login_required
def equipment_maintenance(id):
    eq = Equipment.query.get_or_404(id)
    requests = MaintenanceRequest.query.filter_by(equipment_id=id).all()
    return render_template('equipment_requests.html', equipment=eq, requests=requests)

@app.route('/calendar')
@login_required
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

@app.route('/employee_lookup')
@login_required
def employee_lookup():
    return render_template('employee_lookup.html')

@app.route('/api/employee/<employee_id>')
@login_required
def get_employee(employee_id):
    employee = Employee.query.filter_by(employee_id=employee_id).first()
    if employee:
        return jsonify({
            'success': True,
            'data': {
                'name': employee.name,
                'employee_id': employee.employee_id,
                'department': employee.department,
                'position': employee.position,
                'email': employee.email,
                'joining_date': employee.joining_date.strftime('%Y-%m-%d')
            }
        })
    return jsonify({'success': False, 'message': 'Employee not found'}), 404

if __name__ == "__main__":
    app.run(debug=True)
