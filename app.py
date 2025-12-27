from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import re
from config import Config
from extensions import db
from models import *
from datetime import date, datetime

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.context_processor
def inject_globals():
    return {
        'now': datetime.utcnow(),
        'date': date,
        'datetime': datetime,
        'current_date': datetime.now().strftime('%B %d, %Y')
    }

@app.route('/')
@login_required
def dashboard():
    from sqlalchemy import func
    
    # 1. Critical Equipment (Health < 30)
    critical_eq_count = Equipment.query.filter(Equipment.health_score < 30).count()
    
    # 2. Active Requests (not completed/scrapped)
    active_req_count = MaintenanceRequest.query.filter(MaintenanceRequest.stage.notin_(['Repaired', 'Scrap'])).count()
    tech_load = min(int((active_req_count / 5) * 100), 100)
    
    # 3. Open Requests
    pending_count = MaintenanceRequest.query.filter(MaintenanceRequest.stage.in_(['New', 'In Progress'])).count()
    overdue_count = MaintenanceRequest.query.filter(
        MaintenanceRequest.stage.notin_(['Repaired', 'Scrap']),
        MaintenanceRequest.scheduled_date < date.today()
    ).count()
    
    # 4. Completed count
    completed_count = MaintenanceRequest.query.filter(MaintenanceRequest.stage == 'Repaired').count()

    # 5. Team reports - convert to list of tuples for JSON serialization
    team_reports_raw = db.session.query(MaintenanceRequest.team, func.count(MaintenanceRequest.id)).group_by(MaintenanceRequest.team).all()
    team_reports = [(t[0], t[1]) for t in team_reports_raw]
    
    dept_reports_raw = db.session.query(Equipment.department, func.count(MaintenanceRequest.id)).join(MaintenanceRequest, Equipment.id == MaintenanceRequest.equipment_id).group_by(Equipment.department).all()
    dept_reports = [(d[0], d[1]) for d in dept_reports_raw]
    
    # 6. Recent requests (last 10)
    recent_requests = MaintenanceRequest.query.order_by(MaintenanceRequest.created_at.desc()).limit(10).all()
    
    # 7. All active requests for report
    all_requests = MaintenanceRequest.query.order_by(MaintenanceRequest.created_at.desc()).all()
    
    # 8. Status distribution for chart
    status_counts = db.session.query(MaintenanceRequest.stage, func.count(MaintenanceRequest.id)).group_by(MaintenanceRequest.stage).all()
    status_data = {stage: count for stage, count in status_counts}
    
    # 9. Teams data for report - convert to list of tuples
    teams_data_raw = db.session.query(
        MaintenanceRequest.team,
        func.count(MaintenanceRequest.id).label('total'),
        func.sum(db.case((MaintenanceRequest.stage == 'Repaired', 1), else_=0)).label('completed')
    ).group_by(MaintenanceRequest.team).all()
    teams_data = [(t[0], t[1], t[2] or 0) for t in teams_data_raw]
    
    return render_template('dashboard.html', 
                           team_reports=team_reports, 
                           dept_reports=dept_reports,
                           critical_eq_count=critical_eq_count,
                           tech_load=tech_load,
                           pending_count=pending_count,
                           overdue_count=overdue_count,
                           completed_count=completed_count,
                           active_req_count=active_req_count,
                           recent_requests=recent_requests,
                           all_requests=all_requests,
                           status_data=status_data,
                           teams_data=teams_data)

@app.route('/work_centers')
@login_required
def list_work_centers():
    work_centers = WorkCenter.query.all()
    return render_template('work_centers.html', work_centers=work_centers)

@app.route('/teams')
@login_required
def teams():
    # Use distinct to avoid duplicates if migration ran twice
    teams = MaintenanceTeam.query.group_by(MaintenanceTeam.team_name).all()
    team_members = {}
    active_request_counts = {}
    
    for team in teams:
        # Get Members
        members = Technician.query.filter_by(team_id=team.id).all()
        team_members[team.team_name] = members
        
        # Get Request Count
        # Count requests where team matches team name and stage is not closed
        count = MaintenanceRequest.query.filter(
            MaintenanceRequest.team == team.team_name,
            MaintenanceRequest.stage.notin_(['Repaired', 'Scrap'])
        ).count()
        active_request_counts[team.team_name] = count
        
    return render_template('teams.html', teams=teams, team_members=team_members, active_request_counts=active_request_counts)

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
        # Handle optional integer fields
        wc_id = request.form.get("work_center_id")
        wc_id = int(wc_id) if wc_id else None
        
        eq = Equipment(
            name=request.form["name"],
            serial_number=request.form["serial"],
            department=request.form["department"],
            assigned_employee=request.form["employee"],
            employee_id=request.form.get("employee_id"),
            maintenance_team=request.form["team"],
            default_technician=request.form["technician"],
            location=request.form["location"],
            work_center_id=wc_id
        )
        db.session.add(eq)
        db.session.commit()
        flash("New Equipment Added Successfully!", "success")
        return redirect("/equipment")

    all_equipment = Equipment.query.all()
    for eq in all_equipment:
        eq.open_requests_count = MaintenanceRequest.query.filter(
            MaintenanceRequest.equipment_id == eq.id,
            MaintenanceRequest.stage.notin_(["Repaired", "Scrap"])
        ).count()
        
    work_centers = WorkCenter.query.all()
    return render_template("equipment.html", equipment=all_equipment, work_centers=work_centers)

@app.route("/create_request", methods=["GET", "POST"])
@login_required
def create_request():
    equipment = Equipment.query.all()
    pre_date = request.args.get('date', '')
    pre_type = request.args.get('type', 'Corrective')

    if request.method == "POST":
        maintenance_for = request.form.get("maintenance_for", "Equipment")
        
        try:
            priority = int(request.form.get("priority", 0))
        except:
            priority = 0
            
        try:
            duration = float(request.form.get("duration", 0.0))
        except:
            duration = 0.0

        req = MaintenanceRequest(
            subject=request.form["subject"],
            request_type=request.form.get("type", "Corrective"),
            maintenance_for=maintenance_for,
            priority=priority,
            duration=duration,
            scheduled_date=None
        )

        if maintenance_for == "Equipment":
            eq = Equipment.query.get(request.form["equipment_id"])
            req.equipment_id = eq.id
            req.equipment_name = eq.name
            req.team = eq.maintenance_team
            req.technician = eq.default_technician
        else:
            wc_id = request.form.get("work_center_id")
            if wc_id:
                wc = WorkCenter.query.get(wc_id)
                req.work_center_id = wc.id
                req.equipment_name = wc.name 
                req.team = "Maintenance" 
                req.technician = "Unassigned"
            else:
                # Fallback if WC not selected
                req.equipment_name = "Unknown Work Center"
        
        if request.form.get("scheduled_date"):
            date_str = request.form.get("scheduled_date")
            try:
                if 'T' in date_str:
                    req.scheduled_date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M').date()
                else:
                    req.scheduled_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                pass 

        db.session.add(req)
        db.session.commit()
        flash("Maintenance Request Created Successfully!", "success")
        return redirect("/kanban")

    work_centers = WorkCenter.query.all()
    today_date = date.today().strftime('%m/%d/%Y')
    return render_template("request_form.html", equipment=equipment, work_centers=work_centers, pre_date=pre_date, pre_type=pre_type, today_date=today_date)

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
    
    if new_stage == "Scrap":
        if req.equipment_id:
            eq = Equipment.query.get(req.equipment_id)
            if eq:
                eq.is_scrapped = True
            
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
    # Show ALL requests
    all_requests = MaintenanceRequest.query.all()
    events = []
    for req in all_requests:
        if req.scheduled_date:
            color = '#28a745' if req.request_type == 'Preventive' else '#dc3545'
            events.append({
                'title': f"{req.equipment_name}: {req.subject}",
                'start': req.scheduled_date.isoformat(),
                'date': req.scheduled_date.isoformat(), # For new calendar
                'type': req.request_type, # For new calendar logic
                'id': req.id,
                'color': color
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
