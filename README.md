◉ OWL — Bird Vocalization Archive
Setup & Reference Guide
================================================================================

# OVERVIEW

A public, community-driven web archive of bird vocalizations built with Flask
and PostgreSQL. Anyone can browse; registered contributors manage their own
species records and audio samples.

## FEATURES

• Public archive — browse birds and listen to audio without an account
• User accounts — register with a profile picture; each user gets a unique
tag (e.g. JOSH#N77B)
• Bird records — species entries with images and descriptions
• Audio samples — multiple recordings per species, categorized by
vocalization type (song, call, alarm, mating, contact, flight, feeding, other)
• Hide / Delete — owners can hide content from the public or permanently
remove it
• Downloadable images — optional per-bird image download toggle
• QR code profiles — every profile page has a scannable QR code
• Native HTML5 audio player — no external dependencies for playback

## TECH STACK

Layer Technology

---

Backend Python 3.11+, Flask 3
ORM SQLAlchemy (Flask-SQLAlchemy)
Auth Flask-Login
Database PostgreSQL (SQLite works for dev)
Templates Jinja2
Styling Vanilla CSS (custom design system, no framework)
Fonts Syne, Space Mono, Inter (Google Fonts)
QR Codes qrcode + Pillow
File uploads Werkzeug (built into Flask)

## PROJECT STRUCTURE

owl/
├── app.py # App factory, error handlers
├── config.py # Configuration (reads .env)
├── extensions.py # db, login_manager instances
├── models.py # User, Bird, AudioSample models
├── utils.py # File save/delete helpers, tag generator
├── requirements.txt
├── .env.example
├── .gitignore
│
├── auth/
│ ├── **init**.py
│ └── routes.py # /signup /login /logout
│
├── birds/
│ ├── **init**.py
│ └── routes.py # /bird/create /bird/<id>/edit|delete|hide
│
├── audios/
│ ├── **init**.py
│ └── routes.py # /audio/<bird_id>/upload /audio/<id>/edit|delete|hide
│
├── public/
│ ├── **init**.py
│ └── routes.py # / /bird/<id> /u/<username> /image/<path>
│
├── templates/
│ ├── base.html
│ ├── 404.html
│ ├── 403.html
│ ├── auth/
│ │ ├── login.html
│ │ └── signup.html
│ ├── birds/
│ │ └── bird_form.html
│ ├── audios/
│ │ └── audio_form.html
│ └── public/
│ ├── home.html
│ ├── bird.html
│ └── profile.html
│
└── static/
├── css/
│ └── main.css
├── js/
│ └── main.js
├── img/
│ └── default.png # Default avatar
└── uploads/
├── profile_pics/
├── bird_images/
└── audios/

## PREREQUISITES

• Python 3.11 or higher → python3 --version
• pip → pip3 --version
• PostgreSQL 14+ → psql --version
• git → git --version
• Internet access (to install packages and load Google Fonts)

================================================================================
INSTALLATION — WINDOWS (FRESH MACHINE)
================================================================================

All commands below run in Command Prompt (cmd) — not PowerShell.
Search for "cmd" in the Start menu to open it.

## STEP 1 — INSTALL PYTHON

1. Go to https://www.python.org/downloads/
2. Click "Download Python 3.x.x" (the big yellow button)
3. Run the installer
4. **_ IMPORTANT: Check "Add Python to PATH" before clicking Install Now _**

Verify:
python --version
You should see something like: Python 3.12.3
If you see an error, restart your computer and try again.

## STEP 2 — INSTALL GIT

1. Go to https://git-scm.com/download/win
2. Download the installer (64-bit)
3. Run it — default options are fine, just keep clicking Next
4. Click Finish

Verify:
git --version

## STEP 3 — INSTALL POSTGRESQL

1. Go to https://www.enterprisedb.com/downloads/postgres-postgresql-downloads
2. Download PostgreSQL 16 for Windows x86-64
3. Run the installer — keep all defaults
   (PostgreSQL Server, pgAdmin, Stack Builder, Command Line Tools)
4. When asked for a password, type something memorable — this is the
   postgres superuser password. WRITE IT DOWN.
5. Port: leave as 5432
6. Click through to finish

After installation, PostgreSQL runs automatically as a Windows service.

If "psql" is not recognized, add it to your PATH: 1. Search "Environment Variables" in the Start menu 2. Click "Edit the system environment variables" 3. Click "Environment Variables" 4. Under System variables, find Path → Edit 5. Click New and add: C:\Program Files\PostgreSQL\16\bin 6. Click OK on all windows, close and reopen Command Prompt

## STEP 4 — SET UP THE DATABASE

Connect to PostgreSQL:
psql -U postgres

Enter your password when prompted (you won't see characters — that's normal).
You should see a "postgres=#" prompt.

Run these commands one by one:

    CREATE USER owl_user WITH PASSWORD 'owl_pass';
    CREATE DATABASE owl_db OWNER owl_user;
    GRANT ALL PRIVILEGES ON DATABASE owl_db TO owl_user;
    \q

Verify the connection works:
psql -U owl_user -d owl_db -h localhost
Type "owl_pass" when prompted. You should see "owl_db=>". Type \q to exit.

Tip: You can use a different password — just update owl_pass in .env (Step 6).

## STEP 5 — DOWNLOAD THE PROJECT

Navigate to where you want the project:
cd %USERPROFILE%\Desktop

Clone the project:
git clone https://github.com/your-username/owl.git
cd owl

If you received a ZIP file instead: unzip it, then cd into the folder.
e.g. cd %USERPROFILE%\Desktop\owl

## STEP 6 — CONFIGURE ENVIRONMENT

Copy the example environment file:
copy .env.example .env

Open it in Notepad:
notepad .env

It will look like this:
SECRET_KEY=your-very-secret-key-change-this-in-production
DATABASE_URL=postgresql://owl_user:owl_pass@localhost/owl_db

Generate a strong SECRET_KEY:
python -c "import secrets; print(secrets.token_hex(32))"

Copy the output and paste it as the SECRET_KEY value.
If you used a different password in Step 4, update owl_pass in DATABASE_URL.
Save the file and close Notepad.

## STEP 7 — CREATE VIRTUAL ENVIRONMENT

python -m venv venv

Activate it:
venv\Scripts\activate.bat

Your prompt should now start with (venv):
(venv) C:\Users\YourName\Desktop\owl>

**_ You must run the activation step every time you open a new
Command Prompt to work on this project. _**

## STEP 8 — INSTALL PYTHON PACKAGES

pip install -r requirements.txt

If you see an error about psycopg2, run:
pip install psycopg2-binary --only-binary :all:
Then re-run:
pip install -r requirements.txt

## STEP 9 — RUN THE APP

python app.py

The first run automatically creates all database tables. You should see:
_ Running on http://127.0.0.1:5000
_ Debug mode: on

Open your browser: http://127.0.0.1:5000

## STOPPING & RESTARTING

To stop: press Ctrl + C in Command Prompt

To start again later:
cd %USERPROFILE%\Desktop\owl
venv\Scripts\activate.bat
python app.py

================================================================================
INSTALLATION — LINUX & MACOS
================================================================================

## UBUNTU / DEBIAN

sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv git \
 postgresql postgresql-contrib libpq-dev

## MACOS (WITH HOMEBREW)

/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew update
brew install python postgresql git
brew services start postgresql

## POSTGRESQL SETUP (LINUX/MACOS)

Start the service:
sudo systemctl start postgresql # Ubuntu/Debian
sudo systemctl enable postgresql # auto-start on boot
brew services start postgresql # macOS

Open a PostgreSQL shell:
sudo -u postgres psql # Linux
psql postgres # macOS

Run:
CREATE USER owl_user WITH PASSWORD 'owl_pass';
CREATE DATABASE owl_db OWNER owl_user;
GRANT ALL PRIVILEGES ON DATABASE owl_db TO owl_user;
\q

Verify:
psql -U owl_user -d owl_db -h localhost -c "SELECT 1;" # Should return: ?column? = 1

## PYTHON ENVIRONMENT (LINUX/MACOS)

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

## RUN THE APP

python app.py

# Open: http://127.0.0.1:5000

================================================================================
ENVIRONMENT VARIABLES
================================================================================

Variable Required Description

---

SECRET_KEY Yes Flask session signing key. Use a long random string
in production. Generate with:
python3 -c "import secrets; print(secrets.token_hex(32))"
DATABASE_URL Yes Full PostgreSQL connection string.
Default: postgresql://owl_user:owl_pass@localhost/owl_db

================================================================================
ROUTES REFERENCE
================================================================================

## PUBLIC — NO LOGIN REQUIRED

Method Route Description

---

GET / Home feed — recently added birds
GET /bird/<id> Bird detail page with audio samples
GET /u/<username> User profile page with QR code
GET /image/<filename> Direct download of a bird image
GET /static/uploads/<path> Serve any uploaded file (images, audio)

## AUTHENTICATION

Method Route Description

---

GET/POST /signup Create a new account (with profile picture)
GET/POST /login Sign in
GET /logout Sign out

## BIRD MANAGEMENT — LOGIN REQUIRED

Method Route Description

---

GET/POST /bird/create Add a new species
GET/POST /bird/<id>/edit Edit species details
POST /bird/<id>/delete Permanently delete bird + all audio
POST /bird/<id>/hide Toggle visibility (hide/show)

## AUDIO MANAGEMENT — LOGIN REQUIRED, OWNER ONLY

Method Route Description

---

GET/POST /audio/<bird_id>/upload Upload a new audio sample
GET/POST /audio/<id>/edit Edit audio metadata or replace file
POST /audio/<id>/delete Permanently delete audio sample
POST /audio/<id>/hide Toggle visibility (hide/show)

================================================================================
PERMISSIONS MODEL
================================================================================

Action Owner Visitor

---

View birds & audio Yes Yes
Download images Yes Yes (only if bird.downloadable is true)
Create bird Yes No
Upload audio Yes No
Edit / Delete / Hide Yes No

Ownership check used throughout:
if resource.user_id != current_user.id:
abort(403)

Hide vs Delete:
Hide — sets is_hidden = True. Record stays in the database but is
invisible in all public queries. Owner can still see and toggle it.
Delete — permanently removes the record and all associated files from disk.

All public queries filter hidden content:
Bird.query.filter_by(is_hidden=False)
AudioSample.query.filter_by(is_hidden=False)

================================================================================
FILE STORAGE
================================================================================

Uploaded files are stored locally under static/uploads/:

    static/uploads/
    ├── profile_pics/     ← User avatars
    ├── bird_images/      ← Species photos
    └── audios/           ← Vocalization recordings

Files are renamed to a UUID hex on upload (e.g. 3f8a1c2d...png) to prevent
collisions and avoid exposing original filenames.

Limits:
• Max upload size: 50 MB per request
• Allowed images: png, jpg, jpeg, gif, webp
• Allowed audio: mp3, wav, ogg, flac, m4a, aac

For production, consider moving file storage to S3 or another object store.
Replace save_file() in utils.py with your cloud storage client.

================================================================================
DATABASE SCHEMA
================================================================================

## TABLE: users

Column Type Notes

---

id Integer PK
name String(120) Display name
username String(80) UNIQ URL slug /u/<username>
tag String(20) UNIQ e.g. JOSH#N77B
email String(120) UNIQ
password_hash String(256) Werkzeug pbkdf2
profile_image String(256) Filename in profile_pics/
joined_at DateTime UTC

## TABLE: birds

Column Type Notes

---

id Integer PK
user_id FK → users.id Owner
bird_name String(120)
image_path String(256) Filename in bird_images/
downloadable Boolean Public download allowed
description Text
is_hidden Boolean
created_at DateTime UTC

## TABLE: audio_samples

Column Type Notes

---

id Integer PK
bird_id FK → birds.id Parent species
vocalization_type String(80) song, call, alarm, mating, contact,
flight, feeding, other
description Text
audio_path String(256) Filename in audios/
extra_info Text Optional metadata
is_hidden Boolean
created_at DateTime UTC

================================================================================
DEPLOYMENT
================================================================================

## GUNICORN (PRODUCTION WSGI SERVER)

pip install gunicorn
gunicorn "app:create_app()" --workers 4 --bind 0.0.0.0:8000

## NGINX REVERSE PROXY

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

## SYSTEMD SERVICE (UBUNTU)

Create /etc/systemd/system/owl.service:

    [Unit]
    Description=OWL Bird Vocalization Archive
    After=network.target

    [Service]
    User=www-data
    WorkingDirectory=/path/to/owl
    Environment="PATH=/path/to/owl/venv/bin"
    ExecStart=/path/to/owl/venv/bin/gunicorn "app:create_app()" \
              --workers 4 --bind 127.0.0.1:8000
    Restart=always

    [Install]
    WantedBy=multi-user.target

Then:
sudo systemctl daemon-reload
sudo systemctl enable owl
sudo systemctl start owl

## PRODUCTION CHECKLIST

[ ] Set a strong SECRET_KEY in .env
[ ] Set DEBUG = False
[ ] Use a managed PostgreSQL instance (AWS RDS, Supabase, Render)
[ ] Configure Nginx to serve /static/ directly
[ ] Set client_max_body_size 50M in Nginx for large audio uploads
[ ] Add HTTPS via Let's Encrypt (certbot --nginx)
[ ] Move uploaded files to S3 / object storage for persistence across deploys

================================================================================
TROUBLESHOOTING
================================================================================

"python" is not recognized
Reinstall Python and check "Add Python to PATH". Restart Command Prompt.

"psql" is not recognized
Add C:\Program Files\PostgreSQL\16\bin to your system PATH (see Step 3).

psycopg2 install fails
Windows: pip install psycopg2-binary --only-binary :all:
Ubuntu: sudo apt install libpq-dev python3-dev
pip install psycopg2-binary

FATAL: role "owl_user" does not exist
Re-run the SQL commands in the Database Setup step.

connection refused on port 5432
PostgreSQL is not running.
Windows: Search "Services" → find postgresql-x64-16 → right-click Start
Ubuntu: sudo systemctl start postgresql
macOS: brew services start postgresql

Flash messages don't appear
SECRET_KEY is missing or blank in .env. Ensure no spaces around the = sign.

Uploaded files show as broken images
Create upload folders manually:
mkdir static\uploads\profile_pics (Windows)
mkdir static\uploads\bird_images
mkdir static\uploads\audios
mkdir -p static/uploads/{profile_pics,bird_images,audios} (Linux/macOS)

(venv) not showing in prompt
Run venv\Scripts\activate.bat from inside the owl folder.

Port 5000 already in use
python app.py --port 5001
Then open http://127.0.0.1:5001

ModuleNotFoundError: No module named 'flask'
Virtual environment is not activated.
Run: venv\Scripts\activate.bat (Windows)
source venv/bin/activate (Linux/macOS)

================================================================================
LICENSE
================================================================================

MIT — free to use, modify, and distribute.

◉ OWL — Bird Vocalization Archive
