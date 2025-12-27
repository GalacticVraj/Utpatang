# 🛡️ GearGuard - Industrial Equipment Maintenance System

**GearGuard** is a robust Maintenance Management System designed to streamline equipment tracking, maintenance requests, and technician assignments. Built for the Adani x Odoo Hackathon, it automates the workflow between equipment breakdown and maintenance resolution.

---

## 🚀 Unique Features

### 1. 🏭 Equipment Management
- **Detailed Inventory**: Track equipment name, serial number, department, and location.
- **Smart Assignment**: Link each equipment to a specific **Maintenance Team** and **Default Technician**.
- **Lifecycle Tracking**: Monitor purchase dates, warranty expiry, and scrap status.

### 2. 🔧 Maintenance Request System (The Core)
- **Auto-Fill Logic**: When a user selects a piece of equipment, the system **automatically fetches** and fills the responsible Team and Technician.
- **Request Types**: Supports both **Corrective** (Breakdown) and **Preventive** (Scheduled) maintenance.
- **Status Workflow**: Track requests from `New` -> `In Progress` -> `Completed`.

### 3. 📅 Future Modules (Planned)
- **Kanban Board**: Visual drag-and-drop interface for task management.
- **Calendar View**: Schedule preventive maintenance.

---

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **Database**: SQLite, SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, JavaScript (Jinja2 Templates)
- **Tools**: Flask-Migrate

---

## 📂 Project Structure

```
gearguard/              # Root Project Directory
├── templates/          # HTML Templates
├── static/             # CSS & JS Files
├── instance/           # Database Storage (sqlite)
├── app.py              # Main Application Entry Point
├── models.py           # Database Models
├── config.py           # Configuration Settings
├── extensions.py       # Extensions (DB, Migrate)
├── init_db.py          # Database Initialization Script
└── verify_app.py       # Verification Script
```

> **Note**: All core application files are now in the root directory.

---

## ⚡ Setup & Installation

Follow these steps to get the project running on your local machine.

### 1. Prerequisites
- Python 3.8 or higher installed.

### 2. Installation

1.  **Navigate to the project directory**:
    ```bash
    cd gearguard
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Initialize the Database**:
    We have provided a helper script to set up the tables.
    ```bash
    python init_db.py
    ```

### 3. Running the Application

1.  **Start the Server**:
    ```bash
    python app.py
    ```

2.  **Access the App**:
    Open your browser and go to: `http://127.0.0.1:5000/`

---

## 🧪 Testing

To run the automated verification tests:
```bash
python verify_app.py
```

---

## 🤝 Contribution
1.  Fork the repository.
2.  Create a feature branch.
3.  Commit your changes.
4.  Push to the branch.
5.  Open a Pull Request.
