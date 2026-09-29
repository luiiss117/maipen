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

[0.3.0] - 2026-09-11
### Added
    Database Refactor: Split database.py into separate modules:
        - app/database/__init__.py
        - app/database/user.py
        - app/database/machine.py

    Machine Management:
        Added machine deletion functionality with confirmation handling.

    Account Management:
        Added self-account deletion functionality.

    Service Management:
        Added the ability to create services linked to machines.
        Added service database tables and retrieval logic.
        Added service information display inside machine information pages.
        Added service deletion functionality.

    Docker Deployment:
        Added docker-compose.yml for simplified application deployment.
        Improved Docker configuration for running the Flask application.
        Added Docker container support with persistent application data handling.

### Changed
    Database Architecture:
        Improved database organization by separating user and machine database operations into independent modules.

    Machine Information:
        Fixed machine information retrieval caused by inconsistent UUID variable naming.

    Authentication:
        Imported missing InvalidHashError exception handling in app/routes/auth.py.

    Front-end:
        Updated and improved the UI across all HTML templates.
        Improved delete confirmation pages and overall user interface consistency.

    Application Structure:
        Continued migration toward a modular Flask Blueprint-based architecture.

### Fixed
    Database Bugs:
        Fixed multiple issues in database.py before splitting it into separate modules.

    UUID Handling:
        Fixed incorrect machine retrieval caused by inconsistent UUID variable names.

    Exception Handling:
        Fixed missing InvalidHashError import in authentication routes.

    Data Retrieval:
        Fixed service retrieval and machine-service relationship handling.

### Removed
    Database Cleanup:
        Removed the old database.py file after migrating functionality into app/database modules.

[0.4.0] - 2026-09-29
### Added
    CSRF Protection:
        Added CSRF token validation to POST requests.
    Session Security:
        Improved session handling and security.
    Server-Side Validation:
        Added stronger validation for machine, service, and user input.
    HTTPS:
        Added HTTPS support using the ML-DSA-87 post-quantum signature algorithm.

### Changed
    Authentication:
        Changed unauthenticated access responses from HTTP 404 to HTTP 401.
    Validation:
        Improved server-side validation to prevent invalid or incomplete requests from reaching application logic.
    Security:
        Strengthened request handling, authentication, and session security.

### Fixed
    Machine Registration:
        Fixed KeyError exceptions caused by POST requests missing required fields such as machine name.
    Service Registration:
        Fixed KeyError exceptions caused by POST requests missing required fields.
    Input Validation:
        Fixed multiple validation issues and incorrect validation behavior across the application.
    Request Handling:
        Improved handling of incomplete or malformed POST requests.

### Notes
    Browser Compatibility:
        ML-DSA-87 HTTPS support is not currently supported by Firefox. Chromium-based browsers are recommended when using this configuration.
