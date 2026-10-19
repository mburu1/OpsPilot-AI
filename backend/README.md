# OpsPilot AI - Backend Base Configuration

## Architecture
This backend is built using **Django**, **Django REST Framework**, and **Celery**. It follows a domain-driven design where functionality is split into `apps` and shared logic resides in `platform`.

## Development Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Run migrations: `python manage.py migrate`
3. Start server: `python manage.py runserver`
