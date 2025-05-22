Django Configuration Metadata Management System
Overview:
This project is a Django-based system for managing configuration metadata, with automated Liquibase changelog generation and advanced session/user-based tracking. It is designed for seamless database change management, supporting both per-session and per-user changelog workflows, and appending all changes to a global master changelog.

Features:
Automated Liquibase Changelog Generation
Session-based dummy changelog files (e.g., username-epoch.sql)
Per-user master changelog files (e.g., username-master.sql)
Global master.sql for all changes across all users/sessions
Idempotent and Accurate Migration Tracking
User-friendly UI
"Save all changes to dev" button (visible only when relevant)
Bootstrap-styled and responsive
Django messages for feedback on all actions
Dynamic, Modular Model Support
Handles multiple master entities (Job, Task, State, SIAC, Question, Config)
Auto-incrementing IDs
PostgreSQL JSON/Array field support
Security & Production-Readiness
Session-based file handling
Safe SQL and escaping
Least-privilege DB access

Quick Start:
1. Install Dependencies:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

2. Configure Database:
Set up PostgreSQL and update your settings.py with DB credentials.

3. Run the Server:
python manage.py runserver

4. Liquibase Integration:
Ensure Liquibase CLI is installed (liquibase --version).

5. To apply all changes:
liquibase --changeLogFile=liquibase/changelog/master.sql update

6. Workflow:
Make changes (create/update) to master entities via the Django UI.

7. Changelog files:
Changes are appended to a session-based dummy file (username-epoch.sql).
All changes are also appended to the per-user master (username-master.sql) and the global master.sql.

8. Finalize session:
Click "Save all changes to dev" to finalize and archive the session file (changelog-epoch.sql).
Dummy file is deleted after finalization.
All changes are always available in the per-user and global master files.

9. UI Highlights:
Messages: Success, warning, and error messages are shown at the top of each page.
"Save all changes to dev": Centered button, only visible to authorized users/groups.
Lists: All entity lists are sorted in descending order by primary key.
Security & Best Practices
All SQL is safely generated and escaped.
Changelog session variables are managed per user/session.
Sensitive config (like DB credentials) should be managed using environment variables.

10. Troubleshooting: 
Changelog not found: Ensure you have made a change in the current session before clicking "Save all changes to dev".
SQL errors in Liquibase: Check that all generated SQL values (especially JSON and datetime) are properly quoted and formatted.
File permissions: Ensure your Django process has write access to the changelogfiles directory.

11. Contributing
Fork the repo and create your feature branch.
Commit your changes.
Push to the branch.
Open a Pull Request.
