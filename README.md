# current-events-web-scraper
A Web Scraper for scraping Current Events

## Setup Instructions

### 1. Create Virtual Environment
```bash
python3 -m venv venv
```

### 2. Activate Virtual Environment

**Linux/Mac (bash):**
```bash
source venv/bin/activate
```

**Windows PowerShell:**
```powershell
venv\Scripts\Activate.ps1
```
If you get an execution policy error, run this first:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Create Django Project
```bash
django-admin startproject config .
```

### 5. Create Django App
```bash
python manage.py startapp current_events
```

### 6. Add App to INSTALLED_APPS
Add `'current_events'` to the `INSTALLED_APPS` list in `config/settings.py`

### 7. Run Migrations
```bash
python manage.py migrate
```

### 8. Run Development Server
```bash
python manage.py runserver
```
