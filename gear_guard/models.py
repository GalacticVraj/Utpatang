from extensions import db

# Placeholder for models
# user.py
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    # Add other fields as needed

# equipment.py
class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='available')
    # Add other fields like location, type etc.

# request.py
class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')
