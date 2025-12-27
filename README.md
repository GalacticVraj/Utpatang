# 🛡️ GearGuard: The Ultimate Industrial Maintenance Tracker

GearGuard is a specialized asset management and maintenance workflow system designed for industrial environments. Built with a focus on usability, visual intelligence, and real-time tracking, it streamlines the lifecycle of factory equipment from registration to decommissioning.

## 🚀 Key Features

### 🏭 Asset & Equipment Management
- **Smart Tracking**: Search and filter equipment by name, serial, or department.
- **Maintenance History**: A dedicated "Maintenance" smart button on each equipment row opens a filtered list of all repair jobs for that specific asset.
- **Real-time Badges**: Visual indicator on equipment list showing the count of **open** requests.
- **Automatic Scrap Logic**: Assets are automatically marked as "Scrapped" in the inventory if a maintenance request is moved to the "Scrap" stage.

### 📋 Maintenance Workflow (Kanban)
- **Interactive Board**: Drag-and-drop cards between stages: `New` -> `In Progress` -> `Repaired` -> `Scrap`.
- **Hours Spent Tracking**: Real-time duration logging when a repair is completed.
- **Visual Intelligence**: 
  - **Overdue Indicators**: Automated tagging of past-due repairs with red alerts.
  - **Technician Avatars**: Quick identification of assigned personnel.
  - **Request Ribbons**: Color-coded differentiation between **Corrective** and **Preventive** maintenance.

### 📅 Preventive Maintenance (Calendar)
- **Integrated Scheduling**: A high-level view of all upcoming preventive maintenance tasks.
- **One-Click Creation**: Click any future date on the calendar to pre-fill a preventive maintenance request form for that day.

### 📊 Reporting Dashboard
- **Request Distribution**: Insightful progress bars on the home screen showing maintenance volume across different teams and equipment categories.
- **Real-time KPIs**: Instant visibility into the workload of Mechanics, IT, and Engineering teams.

## 🛠️ Technical Stack
- **Backend**: Python / Flask
- **Database**: SQLAlchemy with SQLite (Flat architecture)
- **Frontend**: Bootstrap 5 + Native HTML5 Drag-and-Drop
- **Libraries**: FullCalendar.js for scheduling visualization

## 🏁 Getting Started

### Installation
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Setup Database
1. Initialize the schema:
   ```bash
   python init_db.py
   ```
2. Populate seed data (Maintenance Teams, Technicians, Sample Equipment):
   ```bash
   python seed_data.py
   ```

### Run Application
```bash
python app.py
```
Access the app at `http://127.0.0.1:5000`

---
*Built for industrial excellence. Built for GearGuard.*
