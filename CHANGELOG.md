# Changelog

## [0.1.0] - 2026-09-05

### Added


    Flask web application with Docker support and a requirements.txt file
    app.py and database.py application scripts
    Web page routing and redirects
    Login, registration, and logout functionality
    Username and password validation
    Session-based authentication and session handling
    Password hashing with Argon2
    Flash messages for user feedback
    SQLite3 database, table, and column creation
    Username and password hash storage in SQLite3
    Foreign key relationships in the SQLite3 database

## [0.2.0] - 2026-09-10

### Added

    Machine Management: Introduced UUIDs for machines and implemented dynamic URL generation in machines.py.
    Validation Logic: Added IP address verification, OS selection options, and unique machine name checks.
    Libraries: Integrated uuid, datetime, and ipaddress into the machine module.

### Changed

    Architecture: Refactored project structure using Blueprints; migrated from a monolithic app.py to a modular structure (/app/database.py, /app/__init__.py, /app/routes/machines.py, /app/routes/auth.py).
    Session Management: Updated session handling to use user_id instead of username for improved security and consistency.
    Database Handling: Implemented with statements in database.py to ensure automatic connection closing; consolidated data retrieval into a central get_user function.
    Front-end: Improved HTML templates in /templates and added Jinja2 redirects across all pages.

### Fixed

    Data Integrity: Corrected credentials.username type from INTEGER to TEXT.
    Authentication Flow: Adjusted the register logic to ensure user validation occurs before password hashing.
    Query Logic: Refined machine selection in /machines to verify both user_id and machine_uid.

### Removed

    Cleanup: Removed redundant variables (is_valid, need_rehash) from app.py.
    Dependencies: Cleaned up requirements.txt by removing unused packages; updated dotenv to python-dotenv.

