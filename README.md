# HRMS Project

A Django-based Human Resource Management System for managing employees, attendance, onboarding, leave requests, and HR/admin workflows.

<img width="1920" height="1080" alt="project image" src="https://github.com/user-attachments/assets/36afe34b-1743-49ed-beb7-60a73705d993" />


## Project Overview

This project includes the following modules:

- `accounts` – admin and HR user management, profiles, and related views
- `employees` – employee records and employee-related functionality
- `attendance` – attendance checks and employee attendance tracking
- `onboarding` – onboarding details, documents, and employee setup
- `leave_management` – leave request handling and approvals
- `dashboard` – dashboard views and reports
- `ai_assistant` – AI assistant, retriever, and vector store based features

## Tech Stack

- Python
- Django
- SQLite (default development database)
- Chroma DB for local vector storage

## Project Structure

```text
hrms_project/
├── accounts/
├── ai_assistant/
├── attendance/
├── chroma_db/
├── dashboard/
├── employees/
├── hrms/
├── leave_management/
├── onboarding/
├── media/
├── static/
├── templates/
├── db.sqlite3
├── manage.py
├── requirements.txt
├── README.md
└── .env
```

## Setup Instructions

1. Create a virtual environment:

```bash
python -m venv venv
```

2. Activate the environment:

On Windows:

```bash
venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Apply database migrations:

```bash
python manage.py migrate
```

5. Create a superuser (optional but recommended):

```bash
python manage.py createsuperuser
```

6. Run the development server:

```bash
python manage.py runserver
```

Then open the app in your browser at:

```text
http://127.0.0.1:8000/
```

## Running Tests

```bash
python manage.py test
```

## Notes

- `db.sqlite3` is the default database for local development.
- The `chroma_db/` directory stores the local Chroma vector database used by the AI assistant module.
- Static and media files are stored in the `static/` and `media/` directories.

## License

This project currently does not include a license file. Add one if you plan to share or publish the project publicly.
