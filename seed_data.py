from app import app, db
from models import MaintenanceTeam, Technician, Equipment, Employee, WorkCenter
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

        if Employee.query.count() == 0:
            employees = [
                Employee(employee_id="EMP001", name="John Doe", department="Maintenance", position="Senior Mechanic", email="john.doe@example.com", joining_date=date(2020, 1, 15)),
                Employee(employee_id="EMP002", name="Jane Smith", department="IT", position="System Admin", email="jane.smith@example.com", joining_date=date(2021, 3, 10)),
                Employee(employee_id="EMP003", name="Robert Brown", department="Production", position="Operator", email="robert.brown@example.com", joining_date=date(2019, 11, 22)),
                Employee(employee_id="EMP004", name="Emily White", department="Engineering", position="Process Engineer", email="emily.white@example.com", joining_date=date(2022, 7, 1)),
                Employee(employee_id="EMP005", name="Michael Green", department="Maintenance", position="Electrician", email="michael.green@example.com", joining_date=date(2021, 5, 5))
            ]
            db.session.add_all(employees)

        db.session.commit()
        print("Data seeded successfully!")


def seed_work_centers():
    wc1 = WorkCenter(name="Assembly 1", code="WC-001", tag="ASM", active_work_centers="Station 1, Station 2", cost_per_hour=50.0, capacity_efficiency=100.0, oee_target=85.0)
    wc2 = WorkCenter(name="Drill 1", code="WC-002", tag="DRL", active_work_centers="Drill Press A", cost_per_hour=35.0, capacity_efficiency=95.0, oee_target=90.0)
    
    db.session.add(wc1)
    db.session.add(wc2)
    db.session.commit()
    print("Work Centers seeded!")

if __name__ == "__main__":
    # seed()
    with app.app_context():
        seed_work_centers()
