# Django Configuration Metadata Management System

A robust Django-based system for managing configuration metadata, with automated Liquibase changelog generation, session-based changelog management, and advanced database change tracking.

---

## 🚀 Features

- **Automated Liquibase Changelog Generation**
  - Session-based SQL changelog files (per user, per session)
  - Per-user master changelog file (accumulates all changes by user)
  - Global `master.sql` (accumulates all changes across users)
  - "Save all changes to dev" button to finalize and copy session changelogs

- **Database Schema Modernization**
  - PostgreSQL native array/JSON fields
  - Auto-incrementing IDs for master entities
  - Cleaned and simplified schema

- **User-Friendly UI**
  - Bootstrap 5 styled forms and tables
  - Centered and context-aware action buttons
  - Real-time error and success messages

- **Security & Best Practices**
  - Session-based tracking for changelogs
  - Safe SQL value formatting and escaping
  - Least-privilege database access

---

## 🏗️ Project Structure

```
config_meta/
├── core/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── viewpage.py
│   ├── utils/
│   │   └── liquibase_changelog.py
│   └── templates/
│       └── viewpages/
├── liquibase/
│   └── changelog/
│       ├── master.sql
│       └── changelogfiles/
│            ├── <user>-<epoch>.sql
│            ├── <user>-master.sql
│            └── changelog-<epoch>.sql
├── manage.py
└── README.md
```

---

## ⚙️ Setup & Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd config_meta
   ```

2. **Create and activate a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure PostgreSQL settings in `settings.py`**

5. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

---

## 🗂️ Liquibase Changelog Automation

- **Session-based changelog files** are created automatically when you make changes through the UI.
- **"Save all changes to dev"** button finalizes the session changelog and copies it to a timestamped file.
- **Per-user master changelog files** (e.g., `username-master.sql`) accumulate all changes by that user.
- **Global master.sql** (`liquibase/changelog/master.sql`) accumulates all changes for all users.

---

## 🛡️ Security & Best Practices

- All SQL values are safely formatted and escaped.
- Only authenticated users can perform changes.
- Changelog files are session- and user-specific to prevent collisions.

---

## 📝 Development & Contribution

- Use feature branches and submit pull requests.
- Run tests before pushing changes.
- Keep dependencies up to date.

---

## 🧪 Testing

- Run all tests:
  ```bash
  python manage.py test
  ```

---

## 💡 Tips

- For production, use a WSGI/ASGI server (not Django’s dev server).
- Regularly backup your `liquibase/changelog` directory.
- Review generated changelogs before applying them to production databases.

---

## 📄 License

MIT License

---

**For questions or contributions, please open an issue or pull request!**


## Overview
This project is a robust and flexible Django web application for managing complex configuration metadata across multiple entities. It features advanced user authentication, dynamic configuration forms, granular permissions, and a modern, user-friendly interface.

---

## Features
- **Configuration Management**: Create, update, and manage metadata for Jobs, Tasks, States, SIACs, Questions, and Configs.
- **Dynamic Forms**: Advanced data transformation and validation for configuration input.
- **User Authentication**: Secure login, logout, and password reset flows using Django's built-in authentication system.
- **Account Management**: Account info modal with password reset, group display, and email notifications for account changes.
- **Role-Based Permissions**: Group-based access control (Product, Developer, etc.), with granular view/edit permissions.
- **Responsive UI**: Clean Bootstrap 5 interface, modals, and dropdowns for settings and account management.
- **Security**: Least privilege, enforced password complexity, server-side permission checks, and session management.
- **Extensible**: Easily add new configuration modules or user roles.

---

## Tech Stack
- Python 3.9+
- Django 4.2.x
- Bootstrap 5.3.x
- Vanilla JavaScript

---

## Setup Instructions

1. **Clone the repository**
    ```bash
    git clone <https://github.com/abhinavsrikanth-yubi/config_meta>
    cd <repo-folder>
    ```

2. **Create and activate a virtual environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure environment variables**
    - Copy `.env.example` to `.env` and set your environment-specific variables (e.g., `SECRET_KEY`, `EMAIL_HOST`, etc.)

5. **Apply migrations**
    ```bash
    python manage.py migrate
    ```

6. **Create a superuser**
    ```bash
    python manage.py createsuperuser
    ```

7. **Run the development server**
    ```bash
    python manage.py runserver
    ```

8. **Access the app**
    - Visit [http://localhost:8000/](http://localhost:8000/) in your browser.

---

## Usage Notes
- Use the gear/settings icon (top-right) for account management and logout.
- Only authenticated users can access configuration pages.
- Group-based permissions restrict access to certain modules and actions.
- Password changes require re-login for security.
- All view pages include the account info modal and settings dropdown for a unified experience.

---

## Folder Structure
```
config_meta/
├── core/
│   ├── templates/
│   │   ├── index.html
│   │   ├── account_info_modals_and_js.html
│   │   └── viewpages/
│   │       ├── job_view.html
│   │       ├── state_view.html
│   │       ├── siac_view.html
│   │       ├── question_view.html
│   │       ├── config_view.html
│   │       └── task_view.html
│   ├── views.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── ...
├── loanos_project/
│   └── settings.py
├── requirements.txt
└── README.md
```

---

## Security & Best Practices
- Do **not** expose your `SECRET_KEY` or sensitive credentials.
- Use environment variables for all secrets and email credentials.
- Regularly review user group assignments and permissions.
- Monitor authentication and account activity logs.
- Keep Django and all dependencies up to date.

---

## Contribution
Pull requests and feature suggestions are welcome! Please open an issue to discuss any major changes.

---
