# Visitor Pass Management System - Mentor Demonstration Guide

This guide provides a comprehensive walkthrough and presentation script for demonstrating **Tasks 1, 2, 3, and 4** to your project mentor or evaluators.

---

## 1. Project Overview & Architecture (What to Explain First)

### What to Tell Your Mentor:
> *"Good morning/afternoon, Mentor. Today we are presenting our **Visitor Pass Management System** (Group 30). We have implemented our core system across four major milestones:*
> 1. *Task 1: Project Setup, clean MVC folder structure, and complete MySQL database design.*
> 2. *Task 2: Database Connectivity layer with 5 robust helper functions and connection-check endpoint.*
> 3. *Task 3: Full Visitor Registration workflow with complete client-server validation and custom design matching our specifications.*
> 4. *Task 4: Complete Login & Session Authentication with role-based dashboard landing pages and clean session clearing on logout."*

---

## 2. Codebase Structure (Where Everything is Located)

Show this project layout in your IDE (VS Code / Antigravity IDE) to demonstrate clean separation of concerns:

```text
MINI PROJECT/
│
├── app.py                      # Thin entry point: configures Flask, SQLAlchemy & registers all blueprints
├── requirements.txt            # Project dependencies (Flask, SQLAlchemy, PyMySQL, dotenv)
├── .env                        # Environment configurations (DB credentials, secret keys)
│
├── database/
│   └── schema.sql              # Table definitions (users, passes, pass_requests, pass_history)
│                               # and default seeded accounts
│
├── models/
│   ├── __init__.py             # Exports db and database helper functions
│   ├── db_helpers.py           # The 5 shared DB helpers with try/rollback/raise logic
│   └── user_model.py           # User data access (get_user_by_email, create_visitor, authenticate_user)
│
├── controllers/
│   ├── __init__.py             # Package initializer
│   ├── main_controller.py      # Root route GET / (redirects to /login)
│   ├── db_controller.py        # GET /test-db (database connectivity health check)
│   ├── auth_controller.py      # GET/POST /register, GET/POST /login, GET /logout
│   └── dashboard_controller.py # Role dashboards (GET /officer/dashboard, GET /visitor/dashboard)
│
├── templates/
│   ├── register.html           # Visitor registration form
│   ├── login.html              # Login form with pale pink card, ID badge icon, and error alerts
│   ├── officer_dashboard.html  # Security Officer landing dashboard (with #officer-dashboard-page)
│   ├── visitor_dashboard.html  # Visitor landing dashboard (with #visitor-dashboard-page)
│   ├── dashboard.html          # Placeholder dashboard page
│   └── passes.html             # Placeholder passes page
│
└── static/
    ├── css/
    │   ├── register.css        # Registration page styling
    │   ├── login.css           # Login page styling (.login-card, .form-group, .btn-login, .message.error)
    │   └── dashboard.css       # Clean, modern role dashboard styles
    ├── js/
    │   └── main.js             # Static JavaScript assets
    └── images/                 # Image assets
```


---

## 3. Step-by-Step Live Demonstration Checklist

### Step 1: Demonstrate Database Schema & Design (Task 1)
**What to Open:** `database/schema.sql` (and optionally MySQL Workbench / CLI)

**What to Point Out:**
1. **Four Core Tables**:
   - `users`: Stores user info (`id`, `name`, `email` [UNIQUE], `password`, `mobile_number`, `role`).
   - `passes`: Master pass records (`id`, `pass_number`, `visitor_type`, `visit_purpose`, `status`).
   - `pass_requests`: Visitor requests linked with foreign keys to `users.id` and `passes.id`.
   - `pass_history`: Processing audit trail linked to `users.id` and `passes.id`.
2. **Default Accounts**:
   - `admin@example.com` / `admin123` &rarr; Role: `Security Officer`
   - `end_user@example.com` / `user123` &rarr; Role: `Visitor`
   - Point out the `ON DUPLICATE KEY UPDATE` clause which ensures the script is idempotent and safe to re-run anytime.

---

### Step 2: Demonstrate the Thin Entry Point (Task 1)
**What to Open:** `app.py`

**What to Point Out:**
- **No business logic in `app.py`**: It strictly handles configuration and initialization.
- **URL Encoding**: Uses `urllib.parse.quote_plus` on MySQL credentials so special symbols in passwords never break the connection string.
- **SQLAlchemy Initialization**: Calls `db.init_app(app)`.
- **Modular Blueprints**: Cleanly registers `main_bp`, `db_bp`, and `auth_bp`.
- **Port**: Configured to run on port `5001`.

---

### Step 3: Demonstrate Database Connectivity & Helpers (Task 2)
**What to Open:** `models/db_helpers.py` and browser at `http://localhost:5001/test-db`

**What to Point Out in Code:**
- The 5 helper functions implemented using `db.session`:
  1. `execute_query(query, params)` &rarr; executes any SQL and commits.
  2. `insert_record(query, params)` &rarr; returns `result.lastrowid`.
  3. `update_record(query, params)` &rarr; returns `result.rowcount`.
  4. `delete_record(query, params)` &rarr; returns `result.rowcount`.
  5. `fetch_records(query, params)` &rarr; runs SELECT and returns rows.
- **Robust Error Handling**: Show that every helper implements the `try ... except SQLAlchemyError: db.session.rollback(); raise error` pattern to guarantee database transaction safety.

**What to Demonstrate in Browser:**
- Open `http://localhost:5001/test-db`.
- Show the mentor the JSON response:
  ```json
  {
    "message": "Database Connected",
    "status": "success"
  }
  ```
- Explain: *"This endpoint runs `SELECT 1` via our SQLAlchemy session, returning HTTP 200 on success and HTTP 500 with diagnostic details if a failure occurs."*

---

### Step 4: Demonstrate Visitor Registration UI & Design (Task 3)
**What to Open:** `http://localhost:5001/` in the browser and `static/css/register.css`

**What to Point Out:**
1. **Root Redirect**: When you hit `http://localhost:5001/`, demonstrate that it automatically performs an HTTP 302 redirect to `/register`.
2. **Design Elements Matching the Requirements**:
   - **Background**: Soft pale pink page background (`#fbebee`).
   - **Card**: Clean, centered white card with smooth rounded corners (`.register-card`).
   - **Top Icon**: Elegant maroon ID card badge icon featuring the person silhouette and ID lines.
   - **Typography & Labels**: Bold labels for `Name`, `Email`, `Password`, `Mobile Number`.
   - **Input Fields**: Light pink input styling (`#fff0f3`) with responsive focus states.
   - **Action Button**: Full-width maroon primary button (`.btn-register`) with hover feedback.
   - **Footer**: Maroon underlined link: *"Already have an account? Login here"*.

---

### Step 5: Demonstrate Validation & Registration Scenarios (Task 3)
**What to Demonstrate Live to the Mentor:**

#### Scenario A: Empty Form Submission
- Leave all fields blank and click the **Register** button.
- **Result to Show**: Red flash error box appears inside the card:
  > **"All fields are required."**
- **Explain to Mentor**: *"HTML5 client-side required attributes were intentionally omitted so empty submits reach our Flask server and trigger our centralized backend validation rules."*

#### Scenario B: Invalid Email Format
- Enter Name: `John Doe`, Email: `johnexample.com` (missing `@`), Password: `password123`, Mobile Number: `9876543210`.
- Click **Register**.
- **Result to Show**:
  > **"Please enter a valid email address."**

#### Scenario C: Duplicate Email Check
- Enter Name: `Admin Clone`, Email: `admin@example.com` (which already exists in the database), Password: `password123`, Mobile Number: `9876543210`.
- Click **Register**.
- **Result to Show**:
  > **"Email already registered."**
- **Explain to Mentor**: *"The server calls `get_user_by_email()` using parameter binding to prevent duplicate account registration and protect against SQL injection."*

#### Scenario D: Successful New Visitor Registration
- Enter new details:
  - Name: `Jane Visitor`
  - Email: `jane.visitor@example.com`
  - Password: `visitorpass123`
  - Mobile Number: `9876543210`
- Click **Register**.
- **Result to Show**: Green flash success box appears inside the card:
  > **"Registration successful. Please login to continue."**

#### Scenario E: Database Verification (Live Proof)
- Open terminal or MySQL Workbench and run:
  ```sql
  SELECT id, name, email, mobile_number, role FROM users WHERE email = 'jane.visitor@example.com';
  ```
- Show the mentor the newly created row with role `Visitor`.

---

### Step 6: Demonstrate Login Page Layout & Root Redirect (Task 4)
**What to Open:** `http://localhost:5001/` in the browser, `templates/login.html`, and `static/css/login.css`

**What to Point Out:**
1. **Root Redirect to /login**:
   - Access `http://localhost:5001/` &rarr; Demonstrate that it immediately triggers an HTTP 302 redirect directly to `/login`.
2. **Matching Visual Layout**:
   - **Background**: Soft pale pink page background (`#fbebee`).
   - **Card**: Centered white card with rounded corners (`.login-card`).
   - **Top Icon**: Maroon ID badge icon (with person silhouette and ID lines).
   - **Header Elements**: Title: *"Visitor Pass"*, Subtitle: *"Login to access your dashboard"*.
   - **Input Fields**: Light pink rounded inputs (`#fff0f3`) for Email (`id="email"`) and Password (`id="password"`).
   - **Login Action**: Full-width maroon button (`id="login-submit-btn"`, `.btn-login`).
   - **Footer Navigation**: Clean footer with *"Don't have an account? Register here"* (`id="register-link"` linking to `/register`).
   - **Clean Experience**: No sample credentials cluttering the UI.

---

### Step 7: Demonstrate Login Validation, Session Management & Role Dashboards (Task 4)
**What to Demonstrate Live to the Mentor:**

#### Scenario A: Empty Credentials Validation
- Leave both Email and Password blank (or enter just email with empty password) and click **Login**.
- **Result to Show**: Red flash alert with class `message error`:
  > **"Email and password are required."**
- **Point out to Mentor**: Form uses `novalidate` without HTML `required` attributes so submissions reach the server-side validator as required by specification.

#### Scenario B: Invalid Credentials Handling
- Enter Email: `admin@example.com` and Password: `wrongpassword`.
- Click **Login**.
- **Result to Show**:
  > **"Invalid email or password."**
- **Explain to Mentor**: `authenticate_user()` performs a safe lookup and returns `None` without leaking whether the email or password was the mismatched field.

#### Scenario C: Security Officer Login & Dashboard Landing
- Enter Security Officer credentials:
  - Email: `admin@example.com`
  - Password: `admin123`
- Click **Login**.
- **Result to Show**:
  - Automatically redirected to **`/officer/dashboard`**.
  - Shows page element with `id="officer-dashboard-page"`.
  - Shows badge *"Security Officer"* and greeting *"Welcome back, Security Officer"*.
  - Displays quick overview cards for pending requests, active passes, and history logs.

#### Scenario D: Role Protection Verification
- While signed in as Security Officer, manually type `http://localhost:5001/visitor/dashboard` into the URL bar.
- **Result to Show**: Automatically denied and redirected back to `/login` because the user's role does not match the Visitor role requirement.

#### Scenario E: Clean Logout & Session Destruction
- Click the **Logout** button (`id="officer-logout-link"`).
- **Result to Show**:
  - Immediately redirects to `/login`.
  - Shows that `session.clear()` and `session.modified = True` destroyed all session keys.
  - Try hitting the browser's Back button or directly typing `http://localhost:5001/officer/dashboard` &rarr; Redirects straight to `/login` because unauthenticated access is blocked!

#### Scenario F: Visitor Login & Dashboard Landing
- Enter Visitor credentials:
  - Email: `end_user@example.com`
  - Password: `user123`
- Click **Login**.
- **Result to Show**:
  - Automatically redirected to **`/visitor/dashboard`**.
  - Shows page element with `id="visitor-dashboard-page"`.
  - Shows badge *"Visitor"* and greeting *"Welcome, Visitor"*.
  - Displays visitor cards: *Request Visitor Pass*, *My Active Passes*, *Pass History*.
- Click **Logout** (`id="visitor-logout-link"`) &rarr; Cleanly clears session and returns to `/login`.

---

## 4. Summary of Task Deliverables (Quick Reference Table)

| Task | Deliverables | Verification Endpoint / Action | Status |
|---|---|---|---|
| **Task 1: Setup & DB Design** | `app.py`, `database/schema.sql`, `requirements.txt`, templates & static scaffolding | `python app.py` on port 5001 | Completed & Verified |
| **Task 2: Database Connectivity** | `models/db_helpers.py` (5 helpers), `controllers/db_controller.py` | `GET http://localhost:5001/test-db` (returns HTTP 200 JSON) | Completed & Verified |
| **Task 3: Registration** | `templates/register.html`, `static/css/register.css`, `models/user_model.py`, `controllers/auth_controller.py` | `GET /register`, full 4-stage validation | Completed & Verified |
| **Task 4: Login & Sessions** | `templates/login.html`, `static/css/login.css`, `templates/officer_dashboard.html`, `templates/visitor_dashboard.html`, `static/css/dashboard.css`, `controllers/dashboard_controller.py`, `controllers/auth_controller.py` | `GET /` &rarr; `/login`, role redirection (`/officer/dashboard`, `/visitor/dashboard`), `/logout` session clear | Completed & Verified |

---

## 5. Potential Questions from Mentor & Recommended Answers

**Q1: How do you prevent SQL injection in your database helpers?**
> *Answer: We use SQLAlchemy's `text()` function with named parameter binding (e.g. `:email`). Parameter values are passed as a dictionary and escaped automatically by the database driver.*

**Q2: What happens if a database operation fails halfway through?**
> *Answer: All our database helpers in `models/db_helpers.py` catch `SQLAlchemyError` and `Exception`, execute `db.session.rollback()` to undo any partial changes, and re-raise the error so callers can gracefully handle it.*

**Q3: Why doesn't the registration or login form use HTML5 required attributes?**
> *Answer: The specifications explicitly required server-side validation to ensure that client manipulation cannot bypass checks, and that empty submissions cleanly display the exact flash message 'Email and password are required.' / 'All fields are required.'*

**Q4: How are user sessions handled and kept secure in Task 4?**
> *Answer: Upon successful authentication with `authenticate_user()`, Flask stores `user_id`, `user_name`, and `role` inside the cryptographically signed `session` cookie powered by `app.config['SECRET_KEY']`. On logout, `session.clear()` and `session.modified = True` remove all session state and force the browser to invalidate the session.*

**Q5: How does the system restrict users from accessing dashboards meant for another role?**
> *Answer: In `controllers/dashboard_controller.py`, each dashboard route inspects the session. If `user_id` is missing or the `role` value does not match the authorized role ('Security Officer' or 'Visitor'), the user is immediately redirected to `/login`.*

**Q6: Why do you use a Python Virtual Environment (`venv`)?**
> *Answer: We use a virtual environment to isolate the project's dependencies (Flask, Flask-SQLAlchemy, PyMySQL) from the global computer environment. This prevents package version conflicts with other projects and ensures that every team member installs identical library versions from requirements.txt.*

**Q7: Why is the `venv/` folder ignored in `.gitignore`?**
> *Answer: A virtual environment contains system-specific compiled binaries and thousands of downloaded files. The best practice is to commit only `requirements.txt`. Each developer can then recreate the exact virtual environment locally in seconds using `python -m venv venv` and `pip install -r requirements.txt`.*


