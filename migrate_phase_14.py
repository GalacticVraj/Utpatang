from app import app, db
from sqlalchemy import text

def migrate():
    with app.app_context():
        # Add work_center_id to Equipment
        try:
            with db.engine.connect() as conn:
                conn.execute(text("ALTER TABLE equipment ADD COLUMN work_center_id INTEGER"))
                print("Added work_center_id to equipment table.")
        except Exception as e:
            print(f"Column work_center_id might already exist in equipment: {e}")

        # Add new columns to Maintenace Request
        new_cols = [
            ("priority", "INTEGER DEFAULT 0"),
            ("duration", "FLOAT DEFAULT 0.0"),
            ("company", "VARCHAR(100) DEFAULT 'My Company (San Francisco)'")
        ]
        
        for col_name, col_type in new_cols:
            try:
                with db.engine.connect() as conn:
                    conn.execute(text(f"ALTER TABLE maintenance_request ADD COLUMN {col_name} {col_type}"))
                    print(f"Added {col_name} to maintenance_request table.")
            except Exception as e:
                print(f"Column {col_name} might already exist: {e}")

if __name__ == "__main__":
    migrate()
