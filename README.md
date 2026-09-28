Maipen

A lightweight Flask-based machine management system for keeping track of machines, operating systems, IP addresses, and services.

Maipen provides a simple web interface where users can register machines, manage services, and maintain an organized inventory.

Features

User authentication

Machine management

Add machines

View machine information

Delete machines

Store:

Machine name

IPv4 address

Operating system

Description

Service management

Add services

Track service ports

Remove services

Account management

SQLite database storage

Docker deployment support

Technology Stack

Python

Flask

SQLite

HTML/CSS

Docker

Docker Compose

Running with Docker
Requirements

Git

Docker

Docker Compose

Clone the repository
git clone https://github.com/luiiss117/maipen.git
cd maipen

Start the application
docker compose up


The application will start on:

http://localhost:5000


To run it in the background:

docker compose up -d

Stopping the application
docker compose down

Project Structure
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

Environment Configuration

Sensitive configuration values should be stored in an environment file.

Example:

.env


Do not commit .env files to Git.

Database

Maipen uses SQLite for storage.

The database is created automatically when the application starts.

Database files are intentionally ignored by Git:

*.db
*.sqlite
*.sqlite3

Security Notes

Protected routes require authentication.

Destructive actions use POST requests instead of GET requests.

User data is isolated through authentication checks.

Session data is stored separately from the application source.

Development

Install dependencies locally:

python -m venv .venv


Activate the environment:

Linux/macOS:

source .venv/bin/activate


Windows:

.venv\Scripts\activate


Install requirements:

pip install -r requirements.txt


Run:

python app.py

License

This project is provided for educational and personal use.
