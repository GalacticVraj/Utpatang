# 🛡️ GearGuard: The Ultimate Industrial Maintenance Tracker (Odoo x Adani)

![License](https://img.shields.io/badge/license-MIT-blue.svg) ![Python](https://img.shields.io/badge/python-v3.8+-blue.svg) ![Flask](https://img.shields.io/badge/framework-Flask-green.svg) ![Status](https://img.shields.io/badge/status-Active-success.svg)

**GearGuard** is a robust, enterprise-grade asset management and maintenance workflow system designed specifically for industrial environments. It bridges the gap between asset tracking and maintenance execution, providing a seamless, visual, and intelligent interface for technicians and facility managers.

---

## 🚀 Key Features

### 1. 📊 Executive Dashboard
Gain instant visibility into your maintenance operations with a real-time command center:
- **Workload Analysis**: Visual progress bars showing request distribution across maintenance teams (Mechanics, Electrical, IT, etc.).
- **Dept. Analytics**: Breakdown of maintenance volume by equipment category/department.
- **KPI Tracking**: Monitor the pulse of your factory floor at a glance.

### 2. 🏭 Advanced Asset & Equipment Management
A centralized "Master Data" repository for all your physical assets.
- **Smart Inventory**: Searchable grid view with filters for Name, Serial Number, and Department.
- **Status Indicators**: Instant visual tags for `Active` vs `Scrapped` assets.
- **Maintenance History**: A dedicated **"Smart Button"** on every equipment record links directly to its full repair history.
- **Visual Alerts**: Real-time **red badges** on equipment cards indicate the number of *open* maintenance requests.
- **Employee Integration**: 
  - **Smart Form**: "Add Equipment" form features an **Employee Lookup** system. Enter an Employee ID (e.g., `EMP002`) to auto-fill their Name and Department, eliminating data entry errors.

### 3. 📋 Intelligent Kanban Workflow
Streamline your repair process with a Trello-style interactive board.
- **Drag-and-Drop**: Move requests effortlessly between stages: `New` ➔ `In Progress` ➔ `Repaired` ➔ `Scrap`.
- **Automated Logic**:
  - **Scrap Trigger**: Dragging a request to the "Scrap" column automatically decomissions the associated equipment in the inventory.
  - **Completion Logging**: Moving a card to "Repaired" prompts the technician to log **Actual Hours** spent.
- **Visual Intelligence**:
  - **Overdue Flags**: Cards for past-due tasks feature a distinct red warning strip.
  - **Technician Avatars**: Quickly identify who is working on what.
  - **Priority Ribbons**: Distinct markers for "Corrective" vs "Preventive" jobs.

### 4. 📅 Preventive Maintenance Calendar
Stay ahead of breakdowns with a dedicated planning view.
- **Monthly/Weekly Views**: See all scheduled preventive maintenance jobs on a calendar grid.
- **One-Click Scheduling**: Click on any future date to instantly open a pre-filled "Preventive Request" form for that specific day.

### 5. 🔍 Employee Database (Temporary DB)
A built-in lightweight database for managing personnel.
- **Quick Lookup**: Dedicated UI to fetch employee details by ID.
- **Data Points**: Stores Name, Department, Position, Email, and Joining Date.
- **Seeded Data**: Comes pre-populated with sample staff for testing (IDs: `EMP001` - `EMP005`).

---

## 🛠️ Technical Architecture

The project is built on a scalable, flat architecture using Python's robust ecosystem.

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Backend** | **Python Flask** | Lightweight, WSGI web application framework. |
| **Database** | **SQLite + SQLAlchemy** | Relational ORM for flexible data modeling and easy migration. |
| **Frontend** | **Bootstrap 5** | Responsive, mobile-first UI framework. |
| **Interactivity** | **JavaScript (ES6)** | Custom logic for Kanban drag-and-drop and API fetch calls. |
| **Scheduling** | **FullCalendar.js** | Interactive calendar component for preventive maintenance. |
| **Styling** | **Custom CSS** | "Odoo-like" professional aesthetic adjustments. |

---

## 📂 Project Structure

```bash
gearguard/
├── app.py                 # Application entry point and route definitions
├── config.py              # Configuration settings (Secret keys, DB URI)
├── extensions.py          # Flask extensions (SQLAlchemy) initialization
├── init_db.py             # Script to initialize database tables
├── seed_data.py           # Script to populate dummy data
├── migrate_db.py          # Helper to handle schema changes
├── models.py              # Database Models (Equipment, Request, Employee, etc.)
├── instance/
│   └── database.db        # SQLite Database file
├── static/
│   ├── css/style.css      # Custom styles
│   └── js/kanban.js       # Drag-and-drop logic
├── templates/             # HTML Templates (Jinja2)
│   ├── base.html          # Base layout
│   ├── dashboard.html     # Home page
│   ├── equipment.html     # Inventory view
│   ├── kanban.html        # Workflow board
│   ├── calendar.html      # Preventive schedule
│   ├── request_form.html  # Create ticket form
│   └── employee_lookup.html # Employee DB search
└── requirements.txt       # Project dependencies
```

---

## 🏁 Getting Started Guide

Follow these steps to set up the GearGuard environment locally.

### Prerequisites
- Python 3.8 or higher installed.

### Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/YourUsername/gearguard.git
    cd gearguard
    ```

2.  **Install Dependencies**
    It's recommended to use a virtual environment.
    ```bash
    pip install -r requirements.txt
    ```

3.  **Initialize the Database**
    Create the necessary tables.
    ```bash
    python init_db.py
    ```

4.  **Seed Demo Data**
    Populate the system with Departments, Technicians, Employees (EMP001-005), and Equipment.
    ```bash
    python seed_data.py
    ```

5.  **Run the Application**
    ```bash
    python app.py
    ```

6.  **Access the App**
    Open your browser and navigate to:
    `http://127.0.0.1:5000`

---

## 📖 User Guide

### How to Add Equipment
1. Go to the **Equipment** page.
2. Click **"Toggle Form"** in the top right.
3. Fill in the Name and Serial Number.
4. **Smart Tip**: In the "Employee ID" field, enter `EMP002` and press `Tab`. Watch the Name and Department auto-fill!
5. Click **"Save Equipment"**.

### How to Process a Request
1. Create a request via the **New Request** page or by clicking a date on the **Calendar**.
2. Go to the **Kanban** board.
3. Drag the card from **New** to **In Progress** when work begins.
4. Drag it to **Repaired** when finished. 
5. *Note: Dragging to **Scrap** will permanently mark the asset as scrapped.*

---

## 🔮 Future Roadmap
- [ ] User Authentication & Role-Based Access Control (RBAC).
- [ ] Email Notifications for Overdue Requests.
- [ ] PDF Report Generation for Maintenance Logs.
- [ ] Mobile-Responsive PWA view for technicians on the floor.

---

*GearGuard v1.0.0 — Built for Excellence.*
