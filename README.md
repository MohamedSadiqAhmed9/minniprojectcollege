# Visitor Pass Management System

**Group 30 - College Mini Project**  
**Tech Stack**: Flask, Python, MySQL, HTML5, CSS3, JavaScript

---

## 📌 Project Overview
The **Visitor Pass Management System** is a web-based application designed to streamline the issuance, verification, and lifecycle management of visitor passes for security officers and visitors.

---

## 🚀 Quick Start Guide

For full cross-platform instructions (Windows, macOS, Linux), refer to **[SETUP_GUIDE.md](SETUP_GUIDE.md)**.

### 1. Clone the repository
```bash
git clone https://github.com/MohamedSadiqAhmed9/minniprojectcollege.git
cd minniprojectcollege
```

### 2. Set up Virtual Environment & Dependencies
```bash
# Create and activate environment
python -m venv venv
.\venv\Scripts\Activate.ps1    # On Windows PowerShell (or source venv/bin/activate on Mac/Linux)

# Install required packages
pip install -r requirements.txt
```

### 3. Set up MySQL Database
1. Open MySQL and create the database:
   ```sql
   CREATE DATABASE IF NOT EXISTS visitor_pass_db;
   ```
2. Import the schema and default accounts:
   ```bash
   mysql -u root -p visitor_pass_db < database/schema.sql
   ```

### 4. Configure Environment
Copy `.env.example` to `.env` and set your MySQL password:
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=visitor_pass_db
SECRET_KEY=visitor-pass-secret-key-2026
PORT=5001
```

### 5. Run the Application
```bash
python app.py
```
Open your browser and visit: **`http://localhost:5001/`**

---

## 📂 Project Structure
```text
├── app.py                      # Application entry point
├── requirements.txt            # Python dependencies
├── .env.example                # Sample environment configuration
├── database/
│   └── schema.sql              # Database schema & default accounts
├── models/
│   ├── __init__.py             # Database initialization & exports
│   ├── db_helpers.py           # Database CRUD helper functions
│   └── user_model.py           # User management queries
├── controllers/
│   ├── main_controller.py      # Root route (redirects to /login)
│   ├── db_controller.py        # Database connection check (/test-db)
│   ├── auth_controller.py      # Registration, login, and logout routes
│   └── dashboard_controller.py # Role-based dashboards (/officer/dashboard, /visitor/dashboard)
├── templates/
│   ├── register.html           # Visitor registration view
│   ├── login.html              # Login view
│   ├── officer_dashboard.html  # Security Officer landing dashboard
│   ├── visitor_dashboard.html  # Visitor landing dashboard
│   ├── dashboard.html          # Generic dashboard view placeholder
│   └── passes.html             # Passes view placeholder
├── static/
│   ├── css/register.css        # Registration page styling
│   ├── css/login.css           # Login page styling
│   ├── css/dashboard.css       # Dashboard landing pages styling
│   ├── js/                     # Static JavaScript
│   └── images/                 # Static Images
├── SETUP_GUIDE.md              # Detailed setup documentation
└── MENTOR_DEMO_GUIDE.md        # Mentor demonstration walkthrough
```

---

## 👥 Default Accounts
- **Security Officer**: `admin@example.com` / `admin123` &rarr; Lands on `/officer/dashboard`
- **Visitor**: `end_user@example.com` / `user123` &rarr; Lands on `/visitor/dashboard`

---

## 🔐 Task 4: Login, Sessions & Role Dashboards
- **Root Redirection**: `GET /` redirects directly to `GET /login`.
- **Authentication**: `POST /login` verifies credentials via `authenticate_user()` and creates a secure session with `user_id`, `user_name`, and `role`.
- **Role-Based Routing**: Security Officers are routed to `/officer/dashboard`, Visitors to `/visitor/dashboard`.
- **Session Cleanup**: `GET /logout` completely clears all session keys (`session.clear()` and `session.modified = True`) and returns to `/login`.
- **Route Protection**: Dashboards automatically reject and redirect unauthenticated or incorrect-role users back to `/login`.

