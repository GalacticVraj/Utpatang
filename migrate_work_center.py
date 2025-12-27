import sqlite3

def migrate():
    conn = sqlite3.connect('instance/database.db')
    cursor = conn.cursor()
    
    # 1. Create WorkCenter table
    try:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS work_center (
            id INTEGER PRIMARY KEY,
            name VARCHAR(100),
            code VARCHAR(50),
            tag VARCHAR(50),
            active_work_centers VARCHAR(200),
            cost_per_hour FLOAT,
            capacity_efficiency FLOAT,
            oee_target FLOAT
        )
        ''')
        print("Table 'work_center' created successfully.")
    except sqlite3.OperationalError as e:
        print(f"Error creating table: {e}")

    # 2. Add health_score to Equipment
    try:
        cursor.execute("ALTER TABLE equipment ADD COLUMN health_score INTEGER DEFAULT 100")
        print("Column 'health_score' added into equipment.")
    except sqlite3.OperationalError as e:
        print(f"Skipping 'health_score': {e}")

    # 3. Add maintenance_for to MaintenanceRequest
    try:
        cursor.execute("ALTER TABLE maintenance_request ADD COLUMN maintenance_for VARCHAR(20) DEFAULT 'Equipment'")
        print("Column 'maintenance_for' added into maintenance_request.")
    except sqlite3.OperationalError as e:
        print(f"Skipping 'maintenance_for': {e}")

    # 4. Add work_center_id to MaintenanceRequest
    try:
        cursor.execute("ALTER TABLE maintenance_request ADD COLUMN work_center_id INTEGER")
        print("Column 'work_center_id' added into maintenance_request.")
    except sqlite3.OperationalError as e:
        print(f"Skipping 'work_center_id': {e}")
        
    conn.commit()
    conn.close()

if __name__ == "__main__":
    migrate()
