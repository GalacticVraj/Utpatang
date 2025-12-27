
import unittest
from app import app, db
from models import Equipment, MaintenanceRequest

class GearGuardTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # Use in-memory DB for testing
        app.config['WTF_CSRF_ENABLED'] = False # Disable CSRF for testing
        
        self.app = app
        self.client = app.test_client()
        
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_equipment(self):
        response = self.client.post('/equipment', data=dict(
            name='Test Drill',
            serial='TD-123',
            department='Construction',
            employee='John Doe',
            team='Alpha',
            technician='Jane Smith',
            location='Site A'
        ), follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        
        # Check if exists in DB
        with app.app_context():
            eq = Equipment.query.filter_by(serial_number='TD-123').first()
            self.assertIsNotNone(eq)
            self.assertEqual(eq.name, 'Test Drill')

    def test_create_request(self):
        # First add equipment
        with app.app_context():
            eq = Equipment(name='Test Crane', serial_number='TC-999', maintenance_team='Beta', default_technician='Bob')
            db.session.add(eq)
            db.session.commit()
            eq_id = eq.id

        # Now create request
        response = self.client.post('/create_request', data=dict(
            subject='Broken Hydraulic',
            type='Corrective',
            equipment_id=eq_id,
            scheduled_date='2025-12-30'
        ), follow_redirects=True)

        self.assertEqual(response.status_code, 200)

        # Check in DB
        with app.app_context():
            req = MaintenanceRequest.query.filter_by(subject='Broken Hydraulic').first()
            self.assertIsNotNone(req)
            self.assertEqual(req.equipment_name, 'Test Crane') # Auto-filled
            self.assertEqual(req.team, 'Beta') # Auto-filled

if __name__ == '__main__':
    unittest.main()
