from extensions import db
from datetime import date

class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    serial_number = db.Column(db.String(100))
    department = db.Column(db.String(50))
    assigned_employee = db.Column(db.String(50))
    location = db.Column(db.String(100))

    maintenance_team = db.Column(db.String(50))
    default_technician = db.Column(db.String(50))

    purchase_date = db.Column(db.Date)
    warranty_expiry = db.Column(db.Date)

    is_scrapped = db.Column(db.Boolean, default=False)

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
    request_type = db.Column(db.String(20))  # Corrective / Preventive

    equipment_id = db.Column(db.Integer)
    equipment_name = db.Column(db.String(100))

    team = db.Column(db.String(50))
    technician = db.Column(db.String(50))

    stage = db.Column(db.String(20), default="New")

    scheduled_date = db.Column(db.Date)
    duration_hours = db.Column(db.Float)

    created_at = db.Column(db.Date, default=date.today)
