# Maipen

# Maipen

A lightweight **Flask-based machine management system** designed for tracking machines, CTF targets and services.

Maipen provides a simple web interface where security consultants, system administrators, and penetration testers can register machines and manage its services.

## Development Status

Maipen is under development.

Some tables, models, and features might already exist even though they are not fully implemented or visible yet. They are there as part of the planned structure and will be used as the project grows.

More features, improvements, and changes will be added over time.

---

## Features

### User Authentication

- User login and authentication
- Protected application routes

### Machine Management

- Add machines
- View machine information
- Delete machines

Each machine stores:

- Machine name
- IPv4 address
- Operating system
- Description

### Service Management

- Add services
- Track service ports
- Remove services

### Account Management

- User account handling
- Authentication-based access control

### Storage

- SQLite database support

### Deployment

- Docker support
- Docker Compose support

---

## Technology Stack

- **Python**
- **Flask**
- **SQLite**
- **HTML/CSS**
- **Docker**
- **Docker Compose**

---

# Running with Docker

## Requirements

Before running Maipen, install:

- Git
- Docker
- Docker Compose

---

## Clone the Repository

```bash
git clone https://github.com/luiiss117/maipen.git
cd maipen
```
## Create the `.env` File

Create a `.env` file inside the `app` directory:

```bash
touch app/.env
```

Generate a secure secret key:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the generated value and add it to app/.env:

```bash
SECRET_KEY=your_generated_key_here
```

Example:

```bash
SECRET_KEY=7f4d2c9e8a1b5f7c3d9e6a4b8c2d1e0f9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4
```

---

## Start the Application

```bash
docker compose up
```

The application will be available at:

```
http://localhost:5000
```

---

## Run in Background

To start Maipen as a background service:

```bash
docker compose up -d
```

---

## Stop the Application

```bash
docker compose down
```

---

# Project Structure

```text
maipen/
│
├── app/
│   ├── database/
│   ├── routes/
│   └── application modules
│
├── templates/
│   ├── login pages
│   ├── machine pages
│   └── service pages
│
├── static/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── app.py
└── README.md
```

---

# Environment Configuration

Sensitive configuration values should be stored in an environment file.

Example:

```text
.env
```

Do **not** commit `.env` files to Git.

Recommended `.gitignore` entry:

```gitignore
.env
```

---

# Database

Maipen uses **SQLite** for persistent storage.

The database is created automatically when the application starts.

Database files are intentionally ignored by Git:

```gitignore
*.db
*.sqlite
*.sqlite3
```

---

# Security Notes

Maipen includes several security measures:

- Protected routes require authentication
- Destructive actions use `POST` requests instead of `GET`
- User data is isolated through authentication checks
- Session data is stored separately from application source code

---

# Development

## Create a Virtual Environment

```bash
python -m venv .venv
```

---

## Activate the Environment

### Linux / macOS

```bash
source .venv/bin/activate
```

### Windows

```powershell
.venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run the Application

```bash
python app.py
```

---

