# ◉ OWL — Bird Vocalization Archive

### Windows Installation Guide

Everything you need to run OWL on a fresh Windows machine — no prior setup assumed.

---

## Table of Contents

1. [What You'll Install](#what-youll-install)
2. [Step 1 — Install Python](#step-1--install-python)
3. [Step 2 — Install Git](#step-2--install-git)
4. [Step 3 — Install PostgreSQL](#step-3--install-postgresql)
5. [Step 4 — Set Up the Database](#step-4--set-up-the-database)
6. [Step 5 — Download the Project](#step-5--download-the-project)
7. [Step 6 — Configure Environment](#step-6--configure-environment)
8. [Step 7 — Create Virtual Environment](#step-7--create-virtual-environment)
9. [Step 8 — Install Python Packages](#step-8--install-python-packages)
10. [Step 9 — Run the App](#step-9--run-the-app)
11. [Stopping & Restarting](#stopping--restarting)
12. [Troubleshooting](#troubleshooting)

---

## What You'll Install

| Software      | Purpose               | Download       |
| ------------- | --------------------- | -------------- |
| Python 3.11+  | Runs the Flask app    | python.org     |
| Git           | Downloads the project | git-scm.com    |
| PostgreSQL 16 | The database          | postgresql.org |

All commands below are run in **Command Prompt (cmd)** — not PowerShell. Search for `cmd` in the Start menu to open it.

---

## Step 1 — Install Python

1. Go to **https://www.python.org/downloads/**
2. Click **Download Python 3.x.x** (the big yellow button)
3. Run the installer
4. **IMPORTANT:** On the first screen, check the box that says **"Add Python to PATH"** before clicking Install Now

Verify it worked — open Command Prompt and type:

```
python --version
```

You should see something like `Python 3.12.3`. If you see an error, restart your computer and try again.

---

## Step 2 — Install Git

1. Go to **https://git-scm.com/download/win**
2. Download the installer (64-bit)
3. Run it — the default options are fine, just keep clicking Next
4. Click Finish

Verify:

```
git --version
```

You should see something like `git version 2.45.0.windows.1`.

---

## Step 3 — Install PostgreSQL

1. Go to **https://www.enterprisedb.com/downloads/postgres-postgresql-downloads**
2. Download **PostgreSQL 16** for Windows x86-64
3. Run the installer
4. When asked to choose components, keep all defaults (PostgreSQL Server, pgAdmin, Stack Builder, Command Line Tools)
5. When asked for a **password**, type something you'll remember — this is the password for the `postgres` superuser. Write it down.
6. Port: leave it as **5432**
7. Locale: leave as default
8. Click through to finish and let it install

After installation, PostgreSQL runs automatically as a Windows service. You don't need to start it manually.

Verify it installed (you may need to open a new Command Prompt window):

```
psql --version
```

If `psql` is not recognized, you need to add it to your PATH manually:

1. Search **"Environment Variables"** in the Start menu
2. Click **"Edit the system environment variables"**
3. Click **"Environment Variables"**
4. Under **System variables**, find **Path** and click **Edit**
5. Click **New** and add: `C:\Program Files\PostgreSQL\16\bin`
6. Click OK on all windows
7. Close and reopen Command Prompt

---

## Step 4 — Set Up the Database

Open Command Prompt and connect to PostgreSQL as the superuser:

```
psql -U postgres
```

It will ask for the password you set during installation. Type it (you won't see any characters — that's normal) and press Enter.

You should now see a `postgres=#` prompt. Run these commands one by one, pressing Enter after each:

```sql
CREATE USER owl_user WITH PASSWORD 'owl_pass';
CREATE DATABASE owl_db OWNER owl_user;
GRANT ALL PRIVILEGES ON DATABASE owl_db TO owl_user;
\q
```

The `\q` exits PostgreSQL. You're back in normal Command Prompt.

Verify the connection works:

```
psql -U owl_user -d owl_db -h localhost
```

Type `owl_pass` when prompted. You should see `owl_db=>`. Type `\q` to exit.

> **Tip:** You can change `owl_pass` to any password you like — just make sure it matches what you put in the `.env` file in Step 6.

---

## Step 5 — Download the Project

Navigate to where you want the project to live. For example, your Desktop:

```
cd %USERPROFILE%\Desktop
```

Clone the project:

```
git clone https://github.com/your-username/owl.git
cd owl
```

> If you received the project as a ZIP file instead: unzip it, then open Command Prompt and use `cd` to navigate into the folder. For example: `cd %USERPROFILE%\Desktop\owl`

---

## Step 6 — Configure Environment

Inside the `owl` folder, there is a file called `.env.example`. Copy it and rename it to `.env`:

```
copy .env.example .env
```

Now open `.env` in Notepad:

```
notepad .env
```

It will look like this:

```
SECRET_KEY=your-very-secret-key-change-this-in-production
DATABASE_URL=postgresql://owl_user:owl_pass@localhost/owl_db
```

You need to replace `your-very-secret-key-change-this-in-production` with a long random string. Generate one by running:

```
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output and paste it as the value for `SECRET_KEY`. The file should end up looking like:

```
SECRET_KEY=4a7f3c9d1e2b8a6f0d5c3e7a9b1f4d2e8c6a0b3f5d1e9c7a2b4f6d8e0a3c5b7
DATABASE_URL=postgresql://owl_user:owl_pass@localhost/owl_db
```

If you used a different password in Step 4, update `owl_pass` in the `DATABASE_URL` too. Save the file and close Notepad.

---

## Step 7 — Create Virtual Environment

Still inside the `owl` folder in Command Prompt, run:

```
python -m venv venv
```

This creates a folder called `venv` that will hold all the Python packages for this project, separate from the rest of your system.

Now activate it:

```
venv\Scripts\activate.bat
```

Your Command Prompt line should now start with `(venv)` like this:

```
(venv) C:\Users\YourName\Desktop\owl>
```

**You need to do this activation step every time you open a new Command Prompt to run the app.**

---

## Step 8 — Install Python Packages

With the virtual environment active (`(venv)` showing), run:

```
pip install -r requirements.txt
```

This will download and install Flask, SQLAlchemy, Flask-Login, the PostgreSQL driver, and everything else the app needs. It may take a minute or two.

If you see an error about `psycopg2`, run this instead:

```
pip install psycopg2-binary --only-binary :all:
```

Then run the full install again:

```
pip install -r requirements.txt
```

---

## Step 9 — Run the App

With your virtual environment still active, run:

```
python app.py
```

The first time you run it, the app will automatically create all the database tables. You should see output like:

```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

Open your browser and go to: **http://127.0.0.1:5000**

OWL is running. You can now sign up, add birds, and upload audio samples.

---

## Stopping & Restarting

**To stop the app:** press `Ctrl + C` in the Command Prompt window.

**To start it again later:**

1. Open Command Prompt
2. Navigate to the project folder:
   ```
   cd %USERPROFILE%\Desktop\owl
   ```
3. Activate the virtual environment:
   ```
   venv\Scripts\activate.bat
   ```
4. Run the app:
   ```
   python app.py
   ```

---

## Troubleshooting

**`python` is not recognized**
You forgot to check "Add Python to PATH" during installation. Uninstall Python, reinstall it, and check that box. Then restart Command Prompt.

**`psql` is not recognized**
PostgreSQL's `bin` folder is not in your PATH. Follow the PATH instructions at the end of Step 3.

**`FATAL: password authentication failed for user "owl_user"`**
The password in your `.env` file doesn't match what you set in Step 4. Open `.env` in Notepad and make sure `owl_pass` in the `DATABASE_URL` matches the password you used when creating the user.

**`connection refused` on port 5432**
PostgreSQL stopped running. Restart it:

1. Search **"Services"** in the Start menu
2. Find **postgresql-x64-16**
3. Right-click → **Start**

**`(venv)` is not showing in Command Prompt**
You haven't activated the virtual environment. Run `venv\Scripts\activate.bat` from inside the `owl` folder.

**Flash messages or login not working**
Your `SECRET_KEY` in `.env` is missing or blank. Make sure it has a value and that there are no spaces around the `=` sign.

**Uploaded files show as broken images**
The `static\uploads` subfolders may not exist. The app creates them automatically on startup — if it's still broken, create them manually:

```
mkdir static\uploads\profile_pics
mkdir static\uploads\bird_images
mkdir static\uploads\audios
```

**Port 5000 already in use**
Something else is using port 5000. Run the app on a different port:

```
python app.py --port 5001
```

Then open **http://127.0.0.1:5001** in your browser.

---

## File Structure Quick Reference

```
owl\
├── app.py              ← Start here: python app.py
├── .env                ← Your secret config (never share this)
├── requirements.txt    ← Python packages list
├── venv\               ← Virtual environment (auto-created)
├── static\
│   └── uploads\        ← All uploaded images and audio files
└── templates\          ← HTML pages
```
