import sqlite3

def migrate():
    conn = sqlite3.connect('instance/database.db')
    cursor = conn.cursor()
    
    # Create User table
    try:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100) UNIQUE,
            password_hash VARCHAR(200)
        )
        ''')
        print("Table 'user' created successfully.")
    except sqlite3.OperationalError as e:
        print(f"Error: {e}")
        
    conn.commit()
    conn.close()

if __name__ == "__main__":
    migrate()
