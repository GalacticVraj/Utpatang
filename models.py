from extensions import db
from datetime import date
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(200))


class WorkCenter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    code = db.Column(db.String(50))
    tag = db.Column(db.String(50))
    active_work_centers = db.Column(db.String(200)) # e.g., "Assembly 1, Drill 1"
    cost_per_hour = db.Column(db.Float, default=0.0)
    capacity_efficiency = db.Column(db.Float, default=100.0)
    oee_target = db.Column(db.Float, default=85.0)

class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    serial_number = db.Column(db.String(100))
    department = db.Column(db.String(50))
    assigned_employee = db.Column(db.String(50))
    employee_id = db.Column(db.String(20)) # Link to Employee table
    location = db.Column(db.String(100))

    maintenance_team = db.Column(db.String(50))
    default_technician = db.Column(db.String(50))

    purchase_date = db.Column(db.Date)
    warranty_expiry = db.Column(db.Date)

    is_scrapped = db.Column(db.Boolean, default=False)
    health_score = db.Column(db.Integer, default=100) # 0-100

class MaintenanceTeam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(50))

class Technician(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    team_name = db.Column(db.String(50))

class MaintenanceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    subject = db.Column(db.String(200))
    maintenance_for = db.Column(db.String(20), default="Equipment") # "Equipment" or "Work Center"
    
    # Polymorphic associations
    equipment_id = db.Column(db.Integer, nullable=True)
    work_center_id = db.Column(db.Integer, nullable=True)
    
    equipment_name = db.Column(db.String(100)) # Stores name of Eq or WC for display

    request_type = db.Column(db.String(20))  # Corrective / Preventive

    team = db.Column(db.String(50))

    technician = db.Column(db.String(50))

    stage = db.Column(db.String(20), default="New")

    scheduled_date = db.Column(db.Date)
    duration_hours = db.Column(db.Float)
    actual_duration = db.Column(db.Float)

    created_at = db.Column(db.Date, default=date.today)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(50))
    position = db.Column(db.String(50))
    email = db.Column(db.String(100))
    joining_date = db.Column(db.Date)
