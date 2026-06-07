# Task Manager - Technical Documentation

## Table of Contents

1. [Overview](#1-overview)
2. [Digitalisation Problems Solved](#2-digitalisation-problems-solved)
3. [Architecture & Technology Stack](#3-architecture--technology-stack)
4. [Project Structure](#4-project-structure)
5. [Data Model](#5-data-model)
6. [Application Modules](#6-application-modules)
7. [User Roles & Permissions](#7-user-roles--permissions)
8. [Feature Reference](#8-feature-reference)
9. [Installation & Deployment](#9-installation--deployment)
10. [User Guide](#10-user-guide)
11. [Configuration](#11-configuration)
12. [Security Considerations](#12-security-considerations)

---

## 1. Overview

Task Manager is a web-based task management application designed for organizational collaboration. It enables teams within any organisation — whether in operations, finance, marketing, human resources, sales, or administration — to create, assign, track, and discuss tasks through a centralised digital platform.

The application follows a lightweight, portable architecture that requires no external database servers, no complex infrastructure, and can be deployed on any machine with Python 3 installed. A single setup script provisions the entire application in under one minute.

### Key Characteristics

- **Organisation-agnostic**: Designed for any type of organisation (corporate, non-profit, governmental, educational), not tied to any specific industry.
- **Portable**: Uses SQLite (file-based database) — no database server installation required. The entire application is self-contained in a single directory.
- **Zero-configuration deployment**: One shell script (`setup.sh`) creates the virtual environment, installs dependencies, initialises the database, and populates it with sample data.
- **No external JavaScript frameworks**: The frontend uses vanilla HTML, CSS, and JavaScript with Jinja2 server-side templating, keeping the application simple and dependency-light.

---

## 2. Digitalisation Problems Solved

### 2.1 Elimination of Paper-Based Task Tracking

**Problem**: Many organisations still track tasks, assignments, and deadlines through paper notebooks, whiteboards, or verbal agreements. This leads to lost information, no audit trail, and difficulty in knowing who is working on what.

**Solution**: The application provides a centralised digital register of all tasks with full metadata (creator, assignee, priority, deadline, status, team). Every change is timestamped, and the complete history of comments and status changes is preserved.

### 2.2 Lack of Visibility Across Departments

**Problem**: In traditional workflows, department managers have limited visibility into what their team members are working on, what is overdue, and how workloads are distributed. Senior management cannot easily assess operational status across the organisation.

**Solution**: The dashboard system provides three levels of visibility:
- **Personal Dashboard**: Each employee sees their own tasks, upcoming deadlines, and recent activity.
- **Manager Overview**: Department managers and team leads see workload distribution across team members, overdue tasks, and task status breakdowns.
- **Admin Analytics**: Platform administrators see organisation-wide statistics including total users, tasks, completion rates, and priority distributions.

### 2.3 Communication Fragmentation

**Problem**: Task-related communication is scattered across emails, phone calls, messaging apps, and verbal conversations. When a new team member inherits a task, they have no context about prior discussions or decisions.

**Solution**: The threaded comment system keeps all task-related discussion attached directly to the task. Comments support @mentions that trigger notifications, ensuring the right people are alerted. Every comment is preserved with the author and timestamp, creating a complete communication record.

### 2.4 Missed Deadlines and Poor Accountability

**Problem**: Without a system that actively surfaces upcoming and overdue deadlines, tasks slip through the cracks. There is no clear record of who was responsible for what.

**Solution**: The application provides:
- Visual deadline indicators on every task (with overdue highlighting in red).
- Upcoming deadlines panel on the personal dashboard.
- Overdue tasks panel on the manager overview.
- In-app and email notifications when deadlines approach.
- Clear creator/assignee attribution on every task.

### 2.5 No Standardised Workflow

**Problem**: Different departments use different methods to track work status — some use spreadsheets, others use email folders, others use nothing. There is no unified way to know whether a task is pending, in progress, under review, or completed.

**Solution**: The application enforces a standardised four-stage workflow: **To Do** → **In Progress** → **Review** → **Done**. The Kanban-style task board provides a visual representation of this workflow, and tasks can be moved between stages via drag-and-drop or button clicks.

### 2.6 Difficulty Onboarding New Tools

**Problem**: Many organisations resist digitalisation because enterprise tools are complex, expensive, require IT support to install, and take weeks to configure.

**Solution**: This application is deliberately simple:
- One command to install (`bash setup.sh`).
- No external services required (no database server, no Redis, no Docker).
- Pre-populated with realistic sample data so users can explore immediately.
- Intuitive interface that mirrors familiar patterns (Kanban boards, comment threads).

---

## 3. Architecture & Technology Stack

### 3.1 Backend

| Component | Technology | Purpose |
|---|---|---|
| Web Framework | Flask 3.0 | HTTP request handling, routing, template rendering |
| ORM | Flask-SQLAlchemy 3.1 | Database abstraction and model definitions |
| Authentication | Flask-Login 0.6 | Session management, login/logout, access control |
| Password Hashing | bcrypt | Secure one-way password hashing |
| Forms/CSRF | Flask-WTF 1.2 | Cross-Site Request Forgery protection |
| Email | Flask-Mail 0.10 | Notification emails (asynchronous via threading) |
| Database | SQLite 3 | File-based relational database |

### 3.2 Frontend

| Component | Technology | Purpose |
|---|---|---|
| Templating | Jinja2 | Server-side HTML rendering with template inheritance |
| Styling | Vanilla CSS | Custom CSS with CSS variables, responsive grid, no frameworks |
| Interactivity | Vanilla JavaScript | Drag-and-drop, AJAX status updates, notification polling, @mention autocomplete |
| Avatars | Gravatar | User avatars based on email hash (no file upload needed) |

### 3.3 Design Pattern

The application uses the **Model-View-Controller (MVC)** pattern implemented through Flask Blueprints:

```
Request → Flask Router → Blueprint Route (Controller) → SQLAlchemy Model → Jinja2 Template (View)
```

Each functional area (auth, tasks, teams, dashboard, profile, admin, notifications) is a separate Blueprint with its own routes, keeping the codebase modular and maintainable.

### 3.4 Request Flow

```
Browser → Flask App → CSRF Check → Login Check → Blueprint Route
   ↓                                                    ↓
Response ← Jinja2 Template ← Context Data ← SQLAlchemy Query
```

For AJAX operations (status changes, notification polling, comment deletion):

```
Browser JS → fetch() → Flask Route → JSON Response → DOM Update
```

---

## 4. Project Structure

```
task_manager/
├── app.py                  # Flask application factory
├── config.py               # Configuration (DB, mail, session)
├── run.py                  # Entry point (python run.py)
├── seed.py                 # Database seeder with sample data
├── setup.sh                # One-command setup script
├── Makefile                # Common commands (run, seed, reset-db)
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
├── app.db                  # SQLite database file (auto-created)
│
├── models/                 # Database models (SQLAlchemy)
│   ├── __init__.py         # DB instance
│   ├── user.py             # User model + team_members association
│   ├── team.py             # Team model
│   ├── task.py             # Task model + Tag model + task_tags
│   ├── comment.py          # Comment model (threaded)
│   └── notification.py     # Notification model
│
├── routes/                 # Blueprint route handlers
│   ├── __init__.py
│   ├── auth.py             # Login, register, logout, password reset
│   ├── tasks.py            # Task CRUD, comments, status changes
│   ├── teams.py            # Team management, membership
│   ├── dashboard.py        # Personal, manager, admin dashboards
│   ├── profile.py          # Profile view/edit, password change
│   ├── admin.py            # User management, platform settings
│   └── notifications.py    # Notification API, email sending
│
├── templates/              # Jinja2 HTML templates
│   ├── layouts/
│   │   └── base.html       # Base layout (navbar, flash messages, scripts)
│   ├── auth/               # Login, register, reset password
│   ├── tasks/              # Task list, create, detail, edit
│   ├── teams/              # Team list, detail, create, edit
│   ├── dashboard/          # Personal, overview, analytics
│   ├── profile/            # View, edit
│   └── admin/              # User management, settings
│
└── static/                 # Static assets
    ├── css/
    │   ├── main.css        # Global styles (600+ lines)
    │   ├── auth.css        # Authentication page styles
    │   └── dashboard.css   # Dashboard and stats styles
    └── js/
        ├── main.js         # CSRF helper, flash auto-dismiss
        ├── tasks.js        # Drag-drop, status change, mentions, search
        └── notifications.js # Notification polling and dropdown
```

---

## 5. Data Model

### 5.1 Entity-Relationship Overview

```
User ──────┐
  │        │ (many-to-many via team_members)
  │        ▼
  │      Team
  │        │
  │        │ (one-to-many)
  │        ▼
  ├──→  Task  ←──── Tag (many-to-many via task_tags)
  │        │
  │        │ (one-to-many)
  │        ▼
  ├──→ Comment (self-referencing for threading)
  │
  └──→ Notification
```

### 5.2 User Model

| Field | Type | Description |
|---|---|---|
| id | Integer, PK | Unique identifier |
| username | String(64), Unique | Login username |
| email | String(120), Unique | Email address (used for Gravatar) |
| password_hash | String(128) | bcrypt-hashed password |
| full_name | String(120) | Display name |
| job_title | String(120) | Professional title |
| department | String(120) | Organisational department |
| bio | Text | Short biography |
| role | String(20) | `user`, `manager`, or `admin` |
| is_active | Boolean | Account active/deactivated |
| notify_assignment | Boolean | Preference: notify on task assignment |
| notify_comments | Boolean | Preference: notify on comments |
| notify_deadlines | Boolean | Preference: notify on deadline approach |
| created_at | DateTime | Registration timestamp |
| last_seen | DateTime | Last activity timestamp |

### 5.3 Team Model

| Field | Type | Description |
|---|---|---|
| id | Integer, PK | Unique identifier |
| name | String(100), Unique | Team name |
| description | Text | Team purpose and scope |
| color | String(7) | Hex colour code for visual identification |
| lead_id | Integer, FK → User | Team lead reference |
| created_at | DateTime | Creation timestamp |

**Membership**: Many-to-many relationship between User and Team via the `team_members` association table.

### 5.4 Task Model

| Field | Type | Description |
|---|---|---|
| id | Integer, PK | Unique identifier |
| title | String(200) | Task title |
| description | Text | Detailed description |
| priority | String(20) | `low`, `medium`, `high`, `critical` |
| status | String(20) | `todo`, `in_progress`, `review`, `done` |
| deadline | DateTime, Nullable | Due date and time |
| creator_id | Integer, FK → User | Who created the task |
| assignee_id | Integer, FK → User, Nullable | Who is responsible |
| team_id | Integer, FK → Team, Nullable | Associated team |
| created_at | DateTime | Creation timestamp |
| updated_at | DateTime | Last modification timestamp |

**Tags**: Many-to-many relationship between Task and Tag via the `task_tags` association table.

### 5.5 Comment Model

| Field | Type | Description |
|---|---|---|
| id | Integer, PK | Unique identifier |
| content | Text | Comment text (supports @mentions) |
| task_id | Integer, FK → Task | Parent task |
| user_id | Integer, FK → User | Comment author |
| parent_id | Integer, FK → Comment, Nullable | Parent comment (for threading) |
| created_at | DateTime | Creation timestamp |

### 5.6 Notification Model

| Field | Type | Description |
|---|---|---|
| id | Integer, PK | Unique identifier |
| user_id | Integer, FK → User | Recipient |
| type | String(50) | `assignment`, `comment`, `deadline`, `overdue` |
| message | String(500) | Human-readable notification text |
| link | String(200) | URL to the relevant page |
| read | Boolean | Read/unread status |
| created_at | DateTime | Creation timestamp |

---

## 6. Application Modules

### 6.1 Authentication Module (`routes/auth.py`)

Handles user registration, login, logout, and password reset.

- **Registration**: Validates username uniqueness, email format, password strength (6+ characters), and password confirmation. Passwords are hashed with bcrypt before storage.
- **Login**: Verifies credentials, checks account active status, supports "remember me" for persistent sessions.
- **Session Management**: Uses Flask-Login with server-side sessions. Session lifetime is 7 days.
- **CSRF Protection**: All POST forms include a CSRF token validated by Flask-WTF.

### 6.2 Task Module (`routes/tasks.py`)

Full CRUD operations for tasks with filtering, comments, and status management.

- **List View**: Displays tasks in a Kanban board (4 columns: To Do, In Progress, Review, Done). Supports filtering by status, priority, assignee, and team. Includes a live search with 500ms debounce.
- **Create/Edit**: Form-based creation with fields for title, description, priority, assignee, team, deadline, and tags. Tags are comma-separated and stored normalised in lowercase.
- **Detail View**: Shows task metadata, description, tags, status change buttons, threaded comments, and a sidebar with assignment details.
- **Status Changes**: Can be done via buttons on the detail page or drag-and-drop on the board. Both use AJAX (fetch API) for instant updates without page reload.
- **Permissions**: Task creators and managers can edit. Task creators and admins can delete.
- **Comments**: Support @mention syntax (`@username`) which triggers in-app and email notifications. Mentions are rendered with blue highlighting. An autocomplete dropdown appears when typing `@` in the comment box.

### 6.3 Teams Module (`routes/teams.py`)

Team management with membership, join/leave, and role-based access.

- **Team List**: Card grid showing team name, colour, member count, open tasks, lead, and member avatars.
- **Team Detail**: Displays member list, open tasks, statistics (total/completed/open), and an "Add Member" form for leads and managers.
- **Membership**: Users can join/leave teams freely. Team leads and managers can add/remove members.
- **Team Creation**: Available to managers and admins. Includes name, description, colour picker, lead selection, and bulk member selection.

### 6.4 Dashboard Module (`routes/dashboard.py`)

Three dashboard views based on user role.

- **Personal Dashboard** (all users): Shows stat cards (total tasks, to do, in progress, done, overdue), task list, team memberships, upcoming deadlines, and recent comment activity.
- **Manager Overview** (managers and admins): Shows organisation-wide task status breakdown, workload distribution bar chart per team member, and overdue tasks list.
- **Admin Analytics** (admins only): Shows platform-wide statistics (users, tasks, comments, teams) and task priority distribution chart.

### 6.5 Notification Module (`routes/notifications.py`)

In-app and email notification system.

- **Triggers**: Notifications are created when:
  - A task is assigned to someone.
  - A comment is posted on a task (notifies creator and assignee).
  - A user is @mentioned in a comment.
- **User Preferences**: Each user can toggle notifications per type (assignments, comments, deadlines) in their profile settings.
- **In-App**: A bell icon in the navbar shows the unread count. Clicking it opens a dropdown with recent notifications. Clicking a notification marks it as read and navigates to the relevant task.
- **Polling**: The frontend polls the `/notifications/unread` endpoint every 30 seconds to update the badge count.
- **Email**: Notifications are also sent via email asynchronously (using Python threading to avoid blocking the request). Uses Flask-Mail with configurable SMTP settings.

### 6.6 Profile Module (`routes/profile.py`)

User profile view and editing.

- **View**: Displays user card (avatar, name, title, department, bio, role, member since, last active), stat cards (tasks assigned, created, completed, completion rate, in progress, comments), a task progress bar, priority breakdown chart, team list, recent tasks, and recent comments.
- **Edit**: Update personal information (full name, email, job title, department, bio), notification preferences, and password.
- **Avatar**: Powered by Gravatar — the avatar is automatically generated based on the user's email hash. No file upload is needed.

### 6.7 Admin Module (`routes/admin.py`)

Platform administration for admin users.

- **User Management**: Table of all users with inline role change (dropdown), activate/deactivate toggle, and registration date.
- **Platform Settings**: Overview of system statistics and configuration.
- **Access Control**: All admin routes are protected by the `@admin_required` decorator which checks for `role == 'admin'`.

---

## 7. User Roles & Permissions

| Action | User | Manager | Admin |
|---|---|---|---|
| View own dashboard | Yes | Yes | Yes |
| Create tasks | Yes | Yes | Yes |
| Edit own tasks | Yes | Yes | Yes |
| Edit any task | No | Yes | Yes |
| Delete own tasks | Yes | Yes | Yes |
| Delete any task | No | No | Yes |
| View team overview | No | Yes | Yes |
| View analytics | No | No | Yes |
| Create teams | No | Yes | Yes |
| Manage team members | No | Yes (+ team leads) | Yes |
| Manage users | No | No | Yes |
| Change user roles | No | No | Yes |
| Activate/deactivate users | No | No | Yes |

---

## 8. Feature Reference

### 8.1 Task Kanban Board

The task list page displays tasks in a four-column Kanban board. Each card shows the task priority badge, title, assignee avatar, deadline, team badge, and tags. Cards can be dragged between columns to change status — the change is persisted via an AJAX call to `/tasks/<id>/status`.

### 8.2 @Mention System

In any comment text area, typing `@` triggers an autocomplete dropdown listing all active users. The dropdown supports:
- **Keyboard navigation**: Arrow keys to move, Enter/Tab to select, Escape to close.
- **Mouse selection**: Click on a username to insert it.
- **Fuzzy matching**: Filters by both username and display name.

When the comment is submitted, the backend parses all `@username` patterns using the regex `@([\w.\-]+)` and creates notifications for each mentioned user. In the rendered comment, mentions are displayed as highlighted blue badges.

### 8.3 Notification Bell

The notification bell icon in the navbar shows the count of unread notifications. Clicking it opens a dropdown that fetches the latest unread notifications from the API. Each notification item can be clicked to mark it as read and navigate to the relevant task. A "Mark all read" button clears all unread notifications at once.

### 8.4 Drag-and-Drop Task Board

Tasks on the Kanban board are draggable HTML elements. When a task card is dropped onto a different column, the JavaScript code:
1. Reads the `data-task-id` from the dragged card.
2. Reads the `data-status` from the target column.
3. Sends a POST request to `/tasks/<id>/status` with the new status.
4. On success, moves the card DOM element and updates column counts.

### 8.5 Team System

Teams represent organisational departments or working groups. Each team has:
- A **lead** (appointed by managers/admins) who can manage membership.
- **Members** who can be added/removed by the lead or managers.
- A **colour** for visual identification across the interface.
- **Associated tasks** that can be filtered on the task board.

Users can freely join or leave teams. The team detail page shows member list, open tasks, and completion statistics.

### 8.6 Profile Statistics

The profile page calculates and displays:
- **Completion rate**: `(tasks done / total assigned) * 100`
- **Task progress bar**: Visual stacked bar showing Done (green), In Progress (blue), and To Do (grey) proportions.
- **Priority breakdown**: Horizontal bar chart of tasks by priority level.

---

## 9. Installation & Deployment

### 9.1 Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- A Unix-like terminal (Linux, macOS, or WSL on Windows)

### 9.2 Quick Start

```bash
cd task_manager
bash setup.sh
source venv/bin/activate
python run.py
```

Open `http://localhost:5000` in a browser.

### 9.3 What setup.sh Does

1. Creates a Python virtual environment in `./venv/`.
2. Installs all dependencies from `requirements.txt`.
3. Copies `.env.example` to `.env` if not present.
4. Runs `seed.py` which:
   - Creates all database tables in `app.db`.
   - Inserts 12 sample users across different departments.
   - Creates 6 teams (Operations, Marketing, Finance, HR, Sales, Administration).
   - Creates 20 realistic tasks with comments, tags, and deadlines.
   - Creates sample notifications.

### 9.4 Sample Accounts

| Username | Password | Role | Department |
|---|---|---|---|
| admin | admin123 | Admin | Administration |
| maria.ionescu | password123 | Manager | Operations |
| andrei.popa | password123 | Manager | Marketing |
| george.tudor | password123 | Manager | Finance |
| elena.radu | password123 | User | Finance |
| cristian.mihai | password123 | User | Sales |
| ana.vasile | password123 | User | Human Resources |
| bogdan.stan | password123 | User | Operations |
| diana.florea | password123 | User | Marketing |
| ioana.barbu | password123 | User | Administration |
| radu.marin | password123 | User | Sales |
| laura.neagu | password123 | User | Legal |

### 9.5 Resetting the Database

```bash
# Delete and re-seed (fresh start with sample data)
make reset-db

# Or manually
rm app.db
source venv/bin/activate
python seed.py
```

### 9.6 Email Testing with Mailpit

The application sends notification emails. For development, use [Mailpit](https://mailpit.axllent.org/) which catches all outgoing emails locally:

1. Install Mailpit (see their website for your OS).
2. Run `mailpit` — it listens on port 1025 (SMTP) and 8025 (web UI).
3. The application is pre-configured to send to `localhost:1025`.
4. Open `http://localhost:8025` to see all captured emails.

### 9.7 Deploying to a VM

The application is designed for instant VM deployment:

```bash
# On a fresh Ubuntu/Debian VM:
sudo apt update && sudo apt install -y python3 python3-venv python3-pip
git clone <repository-url> && cd task_manager
bash setup.sh
source venv/bin/activate
python run.py
```

For production, use a WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 'app:create_app()'
```

---

## 10. User Guide

### 10.1 First Login

1. Open the application in your browser.
2. Enter your username and password on the login screen.
3. You will be taken to your personal dashboard.

### 10.2 Creating a Task

1. Click the **"+ New Task"** button on the dashboard or task list page.
2. Fill in the title (required), description, priority, assignee, team, deadline, and tags.
3. Click **"Create Task"**.
4. If you assign the task to someone, they will receive an in-app notification and an email.

### 10.3 Managing Task Status

**On the task detail page**: Click the status buttons (To Do / In Progress / Review / Done) to change status instantly.

**On the task board**: Drag a task card from one column and drop it onto another column.

### 10.4 Commenting and @Mentions

1. Open any task detail page.
2. Scroll to the comment section at the bottom.
3. Type your comment. To mention a colleague, type `@` followed by their username — a dropdown will appear with suggestions.
4. Select a user from the dropdown (click or press Enter).
5. Click **"Add Comment"**. Mentioned users will be notified.
6. To reply to a specific comment, click **"Reply"** under that comment.

### 10.5 Managing Teams

1. Click **"Teams"** in the navigation bar.
2. Browse existing teams or click **"+ New Team"** (managers/admins only).
3. Click a team card to see its members, open tasks, and statistics.
4. Click **"Join Team"** to become a member, or **"Leave Team"** to depart.
5. Team leads can add/remove members from the team detail page.

### 10.6 Checking Notifications

1. Look at the bell icon in the top-right of the navigation bar.
2. A red badge shows the number of unread notifications.
3. Click the bell to open the notification dropdown.
4. Click a notification to navigate to the relevant task (it will be marked as read).
5. Click **"Mark all read"** to clear all notifications.

### 10.7 Editing Your Profile

1. Click your username/avatar in the navigation bar → **Profile**.
2. Click **"Edit Profile"** to update your name, email, job title, department, and bio.
3. Toggle notification preferences on/off for assignments, comments, and deadlines.
4. Change your password in the password section.

### 10.8 Admin Operations

(Admin users only)

1. Click **"Admin"** in the navigation bar to access user management.
2. Change user roles using the dropdown in the role column.
3. Activate/deactivate accounts using the button in the actions column.
4. Click **"Platform Settings"** for system statistics.

---

## 11. Configuration

All configuration is managed through environment variables (`.env` file) or the `config.py` file.

| Variable | Default | Description |
|---|---|---|
| `SECRET_KEY` | `dev-secret-key...` | Flask session encryption key. **Change in production.** |
| `DATABASE_URL` | `sqlite:///app.db` | Database connection string |
| `MAIL_SERVER` | `localhost` | SMTP server hostname |
| `MAIL_PORT` | `1025` | SMTP server port |
| `MAIL_USE_TLS` | `false` | Enable TLS for SMTP |
| `MAIL_USERNAME` | (empty) | SMTP authentication username |
| `MAIL_PASSWORD` | (empty) | SMTP authentication password |
| `MAIL_DEFAULT_SENDER` | `taskmanager@localhost` | From address for notification emails |

---

## 12. Security Considerations

### Implemented

- **Password Hashing**: All passwords are hashed using bcrypt with automatic salting. Plaintext passwords are never stored.
- **CSRF Protection**: All POST forms include a CSRF token validated by Flask-WTF. AJAX requests include the token in the `X-CSRFToken` header.
- **Session Security**: Server-side sessions via Flask-Login with configurable lifetime.
- **Access Control**: Role-based permissions enforced at the route level with decorators (`@login_required`, `@admin_required`).
- **Input Escaping**: All user content is escaped by Jinja2's auto-escaping before rendering in HTML, preventing XSS attacks.
- **SQL Injection Prevention**: All database queries use SQLAlchemy's parameterised queries — no raw SQL is used.

### Recommendations for Production

- Change `SECRET_KEY` to a cryptographically random string.
- Run behind a reverse proxy (Nginx) with HTTPS.
- Set `PERMANENT_SESSION_LIFETIME` to a shorter duration.
- Configure proper SMTP credentials instead of the Mailpit defaults.
- Set up regular database backups (the `app.db` file).
- Consider adding rate limiting on authentication endpoints.



 make reset-db                                                                
  python run.py