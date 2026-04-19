# ◉ OWL — Bird Vocalization Archive

A public, community-driven web archive of bird vocalizations built with Flask and PostgreSQL. Anyone can browse; registered contributors manage their own species records and audio samples.

---

## Table of Contents

1. [Features](#features)
2. [Tech Stack](#tech-stack)
3. [Project Structure](#project-structure)
4. [Prerequisites](#prerequisites)
5. [Installation — Fresh Machine](#installation--fresh-machine)
   - [1. System Dependencies](#1-system-dependencies)
   - [2. PostgreSQL Setup](#2-postgresql-setup)
   - [3. Clone & Configure](#3-clone--configure)
   - [4. Python Environment](#4-python-environment)
   - [5. Database Initialization](#5-database-initialization)
   - [6. Run the App](#6-run-the-app)
6. [Environment Variables](#environment-variables)
7. [Routes Reference](#routes-reference)
8. [Permissions Model](#permissions-model)
9. [File Storage](#file-storage)
10. [Database Schema](#database-schema)
11. [Deployment](#deployment)
12. [Troubleshooting](#troubleshooting)

---

## Features

- **Public archive** — browse birds and listen to audio samples without an account
- **User accounts** — register with a profile picture; each user gets a unique tag (e.g. `JOSH#N77B`)
- **Bird records** — species entries with images and descriptions
- **Audio samples** — multiple recordings per species, each categorized by vocalization type (song, call, alarm, mating, contact, flight, feeding, other)
- **Hide / Delete** — owners can hide content from the public or permanently remove it
- **Downloadable images** — optional per-bird image download toggle
- **QR code profiles** — every profile page has a scannable QR code linking to it
- **Native HTML5 audio player** — no external dependencies for playback

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11+, Flask 3 |
| ORM | SQLAlchemy (Flask-SQLAlchemy) |
| Auth | Flask-Login |
| Database | PostgreSQL (SQLite works for dev) |
| Templates | Jinja2 |
| Styling | Vanilla CSS (custom design system, no framework) |
| Fonts | Syne, Space Mono, Inter (Google Fonts) |
| QR Codes | `qrcode` + `Pillow` |
| File uploads | Werkzeug (built into Flask) |

---

## Project Structure

```
owl/
├── app.py                  # App factory, error handlers
├── config.py               # Configuration (reads .env)
├── extensions.py           # db, login_manager instances
├── models.py               # User, Bird, AudioSample models
├── utils.py                # File save/delete helpers, tag generator
├── requirements.txt
├── .env.example
├── .gitignore
│
├── auth/
│   ├── __init__.py
│   └── routes.py           # /signup  /login  /logout
│
├── birds/
│   ├── __init__.py
│   └── routes.py           # /bird/create  /bird/<id>/edit|delete|hide
│
├── audios/
│   ├── __init__.py
│   └── routes.py           # /audio/<bird_id>/upload  /audio/<id>/edit|delete|hide
│
├── public/
│   ├── __init__.py
│   └── routes.py           # /  /bird/<id>  /u/<username>  /image/<path>
│
├── templates/
│   ├── base.html
│   ├── 404.html
│   ├── 403.html
│   ├── auth/
│   │   ├── login.html
│   │   └── signup.html
│   ├── birds/
│   │   └── bird_form.html
│   ├── audios/
│   │   └── audio_form.html
│   └── public/
│       ├── home.html
│       ├── bird.html
│       └── profile.html
│
└── static/
    ├── css/
    │   └── main.css
    ├── js/
    │   └── main.js
    ├── img/
    │   └── default.png     # Default avatar
    └── uploads/
        ├── profile_pics/
        ├── bird_images/
        └── audios/
```

---

## Prerequisites

Ensure the following are available on your machine before starting:

- **Python 3.11 or higher** — `python3 --version`
- **pip** — `pip3 --version`
- **PostgreSQL 14+** — `psql --version`
- **git** — `git --version`
- Internet access (to install packages and load Google Fonts in the browser)

---

## Installation — Fresh Machine

### 1. System Dependencies

#### Ubuntu / Debian

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv git postgresql postgresql-contrib libpq-dev
```

#### macOS (with Homebrew)

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

brew update
brew install python postgresql git
brew services start postgresql
```

#### Windows (WSL2 recommended)

Install WSL2 then follow the Ubuntu instructions above. Alternatively use native Windows:
- Python: https://www.python.org/downloads/
- PostgreSQL: https://www.enterprisedb.com/downloads/postgres-postgresql-downloads
- Git: https://git-scm.com/download/win

---

### 2. PostgreSQL Setup

Start the PostgreSQL service:

```bash
# Ubuntu / Debian
sudo systemctl start postgresql
sudo systemctl enable postgresql

# macOS
brew services start postgresql
```

Create the database and user:

```bash
# Open a PostgreSQL shell
sudo -u postgres psql          # Linux
psql postgres                  # macOS
```

Inside the PostgreSQL shell, run:

```sql
CREATE USER owl_user WITH PASSWORD 'owl_pass';
CREATE DATABASE owl_db OWNER owl_user;
GRANT ALL PRIVILEGES ON DATABASE owl_db TO owl_user;
\q
```

> **Tip:** Change `owl_pass` to a strong password and update your `.env` file accordingly.

Verify the connection works:

```bash
psql -U owl_user -d owl_db -h localhost -c "SELECT 1;"
# Should return: ?column? = 1
```

---

### 3. Clone & Configure

```bash
git clone https://github.com/your-username/owl.git
cd owl
```

Copy the example environment file and edit it:

```bash
cp .env.example .env
nano .env          # or: vim .env  |  code .env
```

Set your values:

```env
SECRET_KEY=replace-this-with-a-long-random-string
DATABASE_URL=postgresql://owl_user:owl_pass@localhost/owl_db
```

Generate a strong `SECRET_KEY`:

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

---

### 4. Python Environment

Create and activate a virtual environment:

```bash
python3 -m venv venv

# Activate on Linux / macOS
source venv/bin/activate

# Activate on Windows (CMD)
venv\Scripts\activate.bat

# Activate on Windows (PowerShell)
venv\Scripts\Activate.ps1
```

Install all Python dependencies:

```bash
pip install -r requirements.txt
```

> If `psycopg2-binary` fails to build, try: `pip install psycopg2-binary --no-binary :all:` or install system `libpq-dev` first.

---

### 5. Database Initialization

The app creates all tables automatically on first run. Simply start the app:

```bash
python app.py
```

SQLAlchemy will call `db.create_all()` inside the app context on startup. All three tables (`users`, `birds`, `audio_samples`) will be created in your PostgreSQL database.

Verify:

```bash
psql -U owl_user -d owl_db -h localhost -c "\dt"
# Should list: audio_samples, birds, users
```

---

### 6. Run the App

Development server:

```bash
# Make sure venv is active
source venv/bin/activate

python app.py
```

Open your browser: **http://127.0.0.1:5000**

---

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `SECRET_KEY` | Yes | `owl-secret-key-...` | Flask session signing key. Use a long random string in production. |
| `DATABASE_URL` | Yes | `postgresql://owl_user:owl_pass@localhost/owl_db` | Full PostgreSQL connection string |

---

## Routes Reference

### Public (no login required)

| Method | Route | Description |
|---|---|---|
| GET | `/` | Home feed — recently added birds |
| GET | `/bird/<id>` | Bird detail page with audio samples |
| GET | `/u/<username>` | User profile page with QR code |
| GET | `/image/<filename>` | Direct download of a bird image |
| GET | `/static/uploads/<path>` | Serve any uploaded file (images, audio) |

### Authentication

| Method | Route | Description |
|---|---|---|
| GET/POST | `/signup` | Create a new account (with profile picture) |
| GET/POST | `/login` | Sign in |
| GET | `/logout` | Sign out |

### Bird Management (login required)

| Method | Route | Description |
|---|---|---|
| GET/POST | `/bird/create` | Add a new species |
| GET/POST | `/bird/<id>/edit` | Edit species details |
| POST | `/bird/<id>/delete` | Permanently delete bird + all audio |
| POST | `/bird/<id>/hide` | Toggle visibility (hide/show) |

### Audio Management (login required, owner only)

| Method | Route | Description |
|---|---|---|
| GET/POST | `/audio/<bird_id>/upload` | Upload a new audio sample |
| GET/POST | `/audio/<id>/edit` | Edit audio metadata or replace file |
| POST | `/audio/<id>/delete` | Permanently delete audio sample |
| POST | `/audio/<id>/hide` | Toggle visibility (hide/show) |

---

## Permissions Model

| Action | Owner | Visitor |
|---|---|---|
| View birds & audio | ✅ | ✅ |
| Download images | ✅ | ✅ (if bird.downloadable) |
| Create bird | ✅ | ❌ |
| Upload audio | ✅ | ❌ |
| Edit / Delete / Hide | ✅ | ❌ |

Ownership check used throughout:
```python
if resource.user_id != current_user.id:
    abort(403)
```

**Hide vs Delete:**
- **Hide** — sets `is_hidden = True`; the record stays in the database but is invisible in all public queries. The owner can still see and toggle it.
- **Delete** — permanently removes the record and all associated uploaded files from disk.

All public queries filter hidden content:
```python
Bird.query.filter_by(is_hidden=False)
AudioSample.query.filter_by(is_hidden=False)
```

---

## File Storage

Uploaded files are stored locally under `static/uploads/`:

```
static/uploads/
├── profile_pics/     ← User avatars
├── bird_images/      ← Species photos
└── audios/           ← Vocalization recordings
```

Files are renamed to a UUID hex on upload (e.g. `3f8a1c2d...png`) to prevent collisions and avoid exposing original filenames.

**Limits:**
- Max upload size: **50 MB** per request
- Allowed images: `png`, `jpg`, `jpeg`, `gif`, `webp`
- Allowed audio: `mp3`, `wav`, `ogg`, `flac`, `m4a`, `aac`

For production, consider moving file storage to S3 or another object store. Replace `save_file()` in `utils.py` with your cloud storage client.

---

## Database Schema

### `users`
| Column | Type | Notes |
|---|---|---|
| id | Integer PK | |
| name | String(120) | Display name |
| username | String(80) UNIQUE | URL slug `/u/<username>` |
| tag | String(20) UNIQUE | e.g. `JOSH#N77B` |
| email | String(120) UNIQUE | |
| password_hash | String(256) | Werkzeug pbkdf2 |
| profile_image | String(256) | Filename in `profile_pics/` |
| joined_at | DateTime | UTC |

### `birds`
| Column | Type | Notes |
|---|---|---|
| id | Integer PK | |
| user_id | FK → users.id | Owner |
| bird_name | String(120) | |
| image_path | String(256) | Filename in `bird_images/` |
| downloadable | Boolean | Public download allowed |
| description | Text | |
| is_hidden | Boolean | |
| created_at | DateTime | UTC |

### `audio_samples`
| Column | Type | Notes |
|---|---|---|
| id | Integer PK | |
| bird_id | FK → birds.id | Parent species |
| vocalization_type | String(80) | song, call, alarm, mating, contact, flight, feeding, other |
| description | Text | |
| audio_path | String(256) | Filename in `audios/` |
| extra_info | Text | Optional metadata |
| is_hidden | Boolean | |
| created_at | DateTime | UTC |

---

## Deployment

### Gunicorn (production WSGI server)

```bash
pip install gunicorn
gunicorn "app:create_app()" --workers 4 --bind 0.0.0.0:8000
```

### Nginx reverse proxy (example)

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    client_max_body_size 50M;

    location /static/ {
        alias /path/to/owl/static/;
        expires 30d;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### Systemd service (Ubuntu)

Create `/etc/systemd/system/owl.service`:

```ini
[Unit]
Description=OWL Bird Vocalization Archive
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/owl
Environment="PATH=/path/to/owl/venv/bin"
ExecStart=/path/to/owl/venv/bin/gunicorn "app:create_app()" --workers 4 --bind 127.0.0.1:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable owl
sudo systemctl start owl
```

### Production checklist

- [ ] Set a strong `SECRET_KEY` in `.env`
- [ ] Set `DEBUG = False` (add to `Config` or pass `--no-reload` to gunicorn)
- [ ] Use a managed PostgreSQL instance (e.g. AWS RDS, Supabase, Render)
- [ ] Configure Nginx to serve `/static/` directly
- [ ] Set `client_max_body_size 50M` in Nginx for large audio uploads
- [ ] Add HTTPS via Let's Encrypt (`certbot --nginx`)
- [ ] Move uploaded files to S3 / object storage for persistence across deploys

---

## Troubleshooting

**`psycopg2` install fails**
```bash
sudo apt install libpq-dev python3-dev   # Ubuntu
brew install postgresql                   # macOS
pip install psycopg2-binary
```

**`FATAL: role "owl_user" does not exist`**
You forgot to create the PostgreSQL user. Re-run the SQL commands in [step 2](#2-postgresql-setup).

**`connection refused` on port 5432**
PostgreSQL is not running.
```bash
sudo systemctl start postgresql    # Ubuntu
brew services start postgresql     # macOS
```

**Flash messages don't appear**
Make sure `SECRET_KEY` is set in `.env` and the `.env` file is in the same directory as `app.py`.

**Uploaded files not showing**
Check that the `static/uploads/` subdirectories exist and are writable by the process user. The app creates them on startup but may fail if permissions are wrong:
```bash
chmod -R 755 static/uploads/
```

**`ModuleNotFoundError: No module named 'flask'`**
Your virtual environment is not activated:
```bash
source venv/bin/activate
```

---

## License

MIT — free to use, modify, and distribute.
