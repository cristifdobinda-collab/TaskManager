# Task Manager

A web-based collaborative task management application built with Flask. Teams can create, assign, track, and discuss tasks through a centralised platform — with a Kanban board, threaded comments, @mentions, real-time notifications, and role-based access control.

Built as a licence project by **Cristian Florin Dobinda**.

---

## Features

- **Kanban Board** — drag-and-drop tasks across four stages: To Do, In Progress, Review, Done
- **Task Management** — full CRUD with priority levels, deadlines, tags, assignees, and team association
- **Team System** — organisational teams with leads, members, colour-coded badges, and task filtering
- **Threaded Comments** — @mention autocomplete with keyboard navigation; mentions trigger notifications
- **Notification System** — in-app bell with real-time polling + asynchronous email notifications via SMTP
- **Three-tier Dashboards** — personal view, manager overview (workload distribution), admin analytics
- **Role-based Access Control** — three roles (User, Manager, Admin) with granular permission enforcement
- **User Profiles** — Gravatar avatars, stats (completion rate, priority breakdown), notification preferences
- **Admin Panel** — user management, role changes, account activation/deactivation
- **Zero-config Setup** — one shell script provisions the full environment with sample data in under a minute
- **Security** — bcrypt passwords, CSRF protection on all forms, Jinja2 auto-escape (XSS), SQLAlchemy parameterised queries

---

## Technology Stack

| Layer | Technology |
|---|---|
| Web Framework | Flask 3.0 |
| ORM | Flask-SQLAlchemy 3.1 |
| Authentication | Flask-Login 0.6 |
| Forms / CSRF | Flask-WTF 1.2 |
| Password Hashing | bcrypt |
| Email | Flask-Mail 0.10 |
| Database | SQLite 3 (file-based, no server required) |
| Templating | Jinja2 |
| Frontend | Vanilla HTML, CSS, JavaScript |
| Avatars | Gravatar |

---

## Project Structure

```
task_manager/
├── app.py                  # Flask application factory
├── config.py               # Configuration (DB, mail, session)
├── run.py                  # Entry point
├── seed.py                 # Database seeder with sample data
├── setup.sh                # One-command setup script
├── Makefile                # Common dev commands
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
│
├── models/                 # SQLAlchemy models
│   ├── user.py
│   ├── team.py
│   ├── task.py             # Task + Tag + task_tags
│   ├── comment.py          # Threaded comments
│   └── notification.py
│
├── routes/                 # Flask Blueprints (controllers)
│   ├── auth.py             # Login, register, logout
│   ├── tasks.py            # Task CRUD, comments, status
│   ├── teams.py            # Team management
│   ├── dashboard.py        # Personal / manager / admin views
│   ├── profile.py          # Profile view and edit
│   ├── admin.py            # User management
│   └── notifications.py    # Notification API + email
│
├── templates/              # Jinja2 HTML templates
└── static/                 # CSS and JavaScript
    ├── css/
    └── js/
```

---

## Installation

### Prerequisites

- Python 3.10+
- pip
- Unix-like terminal (Linux, macOS, or WSL on Windows)

### Quick Start

```bash
git clone <repository-url>
cd task_manager
bash setup.sh
source venv/bin/activate
python run.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

`setup.sh` automatically:
1. Creates a Python virtual environment
2. Installs all dependencies
3. Copies `.env.example` to `.env`
4. Initialises the SQLite database
5. Seeds it with 12 sample users, 6 teams, and 20 tasks with comments

---

## Sample Accounts

| Username | Password | Role | Department |
|---|---|---|---|
| `admin` | `admin123` | Admin | Administration |
| `maria.ionescu` | `password123` | Manager | Operations |
| `andrei.popa` | `password123` | Manager | Marketing |
| `george.tudor` | `password123` | Manager | Finance |
| `elena.radu` | `password123` | User | Finance |
| `cristian.mihai` | `password123` | User | Sales |
| `ana.vasile` | `password123` | User | Human Resources |
| `bogdan.stan` | `password123` | User | Operations |
| `diana.florea` | `password123` | User | Marketing |
| `ioana.barbu` | `password123` | User | Administration |
| `radu.marin` | `password123` | User | Sales |
| `laura.neagu` | `password123` | User | Legal |

---

## User Roles & Permissions

| Action | User | Manager | Admin |
|---|---|---|---|
| Create tasks | Yes | Yes | Yes |
| Edit own tasks | Yes | Yes | Yes |
| Edit any task | No | Yes | Yes |
| Delete own tasks | Yes | Yes | Yes |
| Delete any task | No | No | Yes |
| View manager overview | No | Yes | Yes |
| View admin analytics | No | No | Yes |
| Create teams | No | Yes | Yes |
| Manage team members | No | Yes | Yes |
| Manage users / roles | No | No | Yes |

---

## Configuration

All settings are managed via `.env` (created automatically from `.env.example`):

| Variable | Default | Description |
|---|---|---|
| `SECRET_KEY` | `dev-secret-key` | Flask session key — **change in production** |
| `DATABASE_URL` | `sqlite:///app.db` | Database connection string |
| `MAIL_SERVER` | `localhost` | SMTP server |
| `MAIL_PORT` | `1025` | SMTP port |
| `MAIL_USE_TLS` | `false` | Enable TLS |
| `MAIL_USERNAME` | (empty) | SMTP username |
| `MAIL_PASSWORD` | (empty) | SMTP password |
| `MAIL_DEFAULT_SENDER` | `taskmanager@localhost` | From address |

### Email Testing (Development)

[Mailpit](https://mailpit.axllent.org/) captures outgoing emails locally:

```bash
mailpit   # SMTP on :1025, web UI on http://localhost:8025
```

---

## Common Commands

```bash
# Run the application
python run.py

# Reset and re-seed the database
make reset-db

# Run with Gunicorn (production)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 'app:create_app()'
```

---

## Docker

```bash
docker-compose up --build
```

---

## Documentation

Full technical documentation (architecture, data model, module reference, security considerations) is available in [`DOCUMENTATION.md`](DOCUMENTATION.md).

---

## Author

**Cristian Florin Dobinda**  
Licence Project — 2025/2026

---

## License

This project was developed as a university licence (bachelor's thesis) project. All rights reserved by the author.
