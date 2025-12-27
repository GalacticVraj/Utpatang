from app import app, db
from models import MaintenanceTeam, Technician, Equipment
from datetime import date

def seed():
    with app.app_context():
        # Clear existing (optional - for clean start)
        # db.drop_all()
        # db.create_all()

        # Add Teams
        teams = [
            MaintenanceTeam(team_name="Mechanics"),
            MaintenanceTeam(team_name="Electricians"),
            MaintenanceTeam(team_name="IT Support"),
            MaintenanceTeam(team_name="Plumbing")
        ]
        db.session.add_all(teams)

        # Add Technicians
        techs = [
            Technician(name="Mike Hammer", team_name="Mechanics"),
            Technician(name="Sarah Spark", team_name="Electricians"),
            Technician(name="Kevin Bytes", team_name="IT Support"),
            Technician(name="Bob Pipe", team_name="Plumbing"),
            Technician(name="Alice Wrench", team_name="Mechanics")
        ]
        db.session.add_all(techs)

        # Add some initial Equipment if none exists
        if Equipment.query.count() == 0:
            eq1 = Equipment(
                name="CNC Machine X1",
                serial_number="CNC-001",
                department="Production",
                assigned_employee="Vraj",
                location="Floor 1",
                maintenance_team="Mechanics",
                default_technician="Mike Hammer",
                purchase_date=date(2023, 1, 1)
            )
            eq2 = Equipment(
                name="Office Server 7",
                serial_number="SRV-77",
                department="IT",
                assigned_employee="Aditya",
                location="Server Room",
                maintenance_team="IT Support",
                default_technician="Kevin Bytes",
                purchase_date=date(2022, 5, 15)
            )
            db.session.add_all([eq1, eq2])

        db.session.commit()
        print("Data seeded successfully!")

if __name__ == "__main__":
    seed()
