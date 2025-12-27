from app import app, db
from sqlalchemy import text

def migrate():
    with app.app_context():
        try:
            with db.engine.connect() as conn:
                conn.execute(text("ALTER TABLE technician ADD COLUMN team_id INTEGER"))
                print("Added team_id to technician table.")
        except Exception as e:
            print(f"Error adding team_id: {e}")

if __name__ == "__main__":
    migrate()
