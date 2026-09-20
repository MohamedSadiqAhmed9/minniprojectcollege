# Visitor Pass Management System - Team Member Setup Guide

Welcome to the **Visitor Pass Management System** project (Group 30). Follow this step-by-step guide to set up and run the project locally on your machine.

---

## Prerequisites (By Operating System)

### For Windows:
1. **Python (3.10+)**: [Download Python](https://www.python.org/downloads/)
   - *Crucial*: Check the box **"Add python.exe to PATH"** during installation.
2. **MySQL Server & Workbench**: [Download MySQL Installer](https://dev.mysql.com/downloads/installer/)

### For macOS:
1. **Python (3.10+)**: Already included, or install via Homebrew: `brew install python`
2. **MySQL**: Install via Homebrew: `brew install mysql && brew services start mysql` (or download the macOS DMG from [mysql.com](https://dev.mysql.com/downloads/mysql/)).
3. **MySQL Workbench** (optional GUI): [Download for Mac](https://dev.mysql.com/downloads/workbench/)

### For Linux (Ubuntu / Debian):
1. **Python**: `sudo apt update && sudo apt install python3 python3-pip python3-venv`
2. **MySQL**: `sudo apt install mysql-server && sudo systemctl start mysql`

---

## Step-by-Step Setup Instructions

### Step 1: Get the Code
If cloning via Git:
```bash
git clone <your-repository-url>
cd "MINI PROJECT"
```
Or unzip the project files into a folder on your computer.

---

### Step 2: Set Up a Python Virtual Environment (Recommended)
Open your terminal (PowerShell, Command Prompt, or Bash) inside the project folder:

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
*(If you see an execution policy error on PowerShell, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` then activate again).*

**Windows (Command Prompt / cmd):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**Mac / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

> **What are `venv`, `Lib`, and `activate`?**
> - When you run `python -m venv venv`, Python creates an isolated environment folder named `venv/`.
> - **`venv/Lib/site-packages/`**: This is where all project-specific libraries (like Flask, SQLAlchemy, PyMySQL) get downloaded and stored so they don't interfere with your computer's global Python.
> - **`venv/Scripts/` (or `bin/` on Mac)**: Contains the `activate` script (`Activate.ps1` or `activate.bat`). Running it activates the environment, telling your terminal to use this project's isolated libraries and Python binary.
> - **Note**: The `venv/` folder should **never** be pushed to GitHub (it is ignored by `.gitignore`). Every teammate creates their own local `venv` in seconds using the commands above.

---

### Step 3: Install Dependencies
Run the following command to install all required libraries:
```bash
pip install -r requirements.txt
```

This installs:
- `Flask` (Web framework)
- `Flask-SQLAlchemy` (SQLAlchemy integration)
- `PyMySQL` (MySQL driver)
- `python-dotenv` (Environment variable management)
- `cryptography` (Authentication and security)

---

### Step 4: Set Up the MySQL Database

1. Open **MySQL Workbench** or your **MySQL command line**:
   ```bash
   mysql -u root -p
   ```
   *(Enter your local MySQL password when prompted).*

2. Create the database:
   ```sql
   CREATE DATABASE IF NOT EXISTS visitor_pass_db;
   USE visitor_pass_db;
   ```

3. Run the schema file to create the tables and default accounts:
   - In MySQL Workbench: Open file `database/schema.sql` and click the yellow lightning bolt icon (Execute).
   - Or using MySQL CLI:
     ```bash
     mysql -u root -p visitor_pass_db < database/schema.sql
     ```
   - Or run this simple Python one-liner in your terminal:
     ```bash
     python -c "import pymysql; conn=pymysql.connect(host='localhost', user='root', password='YOUR_PASSWORD', database='visitor_pass_db'); cur=conn.cursor(); [cur.execute(s.strip()) for s in open('database/schema.sql').read().split(';') if s.strip()]; conn.commit(); print('Database setup complete!')"
     ```

---

### Step 5: Configure Environment Variables (`.env`)

In the project root folder, check the file named `.env` (or create one if missing):

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=YOUR_MYSQL_PASSWORD_HERE
DB_NAME=visitor_pass_db
SECRET_KEY=visitor-pass-secret-key-2026
PORT=5001
```

> **Note**: Replace `YOUR_MYSQL_PASSWORD_HERE` with the actual password of your local MySQL `root` user (or your MySQL username/password).

---

### Step 6: Run and Verify the Application

1. **Start the Flask app:**
   ```bash
   python app.py
   ```
   You should see output similar to:
   ```text
   * Serving Flask app 'app'
   * Running on http://127.0.0.1:5001
   ```

2. **Verify Database Connection:**
   Open your browser and navigate to:
   [http://localhost:5001/test-db](http://localhost:5001/test-db)
   - Expected output:
     ```json
     {
       "message": "Database Connected",
       "status": "success"
     }
     ```

3. **Open the Application:**
   Navigate to:
   [http://localhost:5001/](http://localhost:5001/)
   - It will automatically redirect to `/register`, displaying the **Visitor Registration** page.

---

## Default Accounts Available in Database
These accounts are automatically seeded in `schema.sql`:
- **Security Officer**:
  - Email: `admin@example.com`
  - Password: `admin123`
  - Role: `Security Officer`
- **Visitor**:
  - Email: `end_user@example.com`
  - Password: `user123`
  - Role: `Visitor`

---

## Troubleshooting Common Issues

1. **"Access denied for user 'root'@'localhost'"**
   - Check the `DB_PASSWORD` inside your `.env` file to ensure it matches your local MySQL server password.

2. **"Can't connect to MySQL server on 'localhost' (10061)"**
   - Make sure your MySQL service is running. On Windows, press `Win + R`, type `services.msc`, find `MySQL` or `MySQL80`, and make sure it is "Running".

3. **Port 5001 Already in Use (Common on macOS)**
   - *On macOS*: macOS uses port 5000/5001 for "AirPlay Receiver" by default. You can disable it in **System Settings > General > AirDrop & AirPlay > Turn off AirPlay Receiver**, OR simply change `PORT=5002` in your `.env` file.
   - *On Windows/Linux*: Change `PORT=5001` in `.env` to `PORT=5002`, or close the program using that port.

---

## Daily Workflow: How to Run the Project Every Time (Quick Cheat Sheet)

Once your setup is finished, here is all you need to do every time you sit down to work or demonstrate:

### 1. Starting Work (2 Commands):
Open your terminal in `MINI PROJECT` and run:

**On Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
python app.py
```

**On Windows (Command Prompt / cmd):**
```cmd
venv\Scripts\activate.bat
python app.py
```

**On macOS & Linux:**
```bash
source venv/bin/activate
python3 app.py
```

*Your browser will now open the project at `http://localhost:5001/`.*

### 2. Stopping Work:
1. In the terminal, press **`Ctrl + C`** to stop the Flask development server.
2. Type **`deactivate`** to exit the virtual environment.


