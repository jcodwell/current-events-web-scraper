# current-events-web-scraper
A Web Scraper for scraping Current Events

## Setup Instructions

### 1. Create Virtual Environment
```bash
python3 -m venv venv
```

### 2. Activate Virtual Environment
```bash
source venv/bin/activate
```

### 3. Install Django
```bash
pip install django
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

### 7. Run Development Server
```bash
python manage.py runserver
```
