from flask import Blueprint

# Import all route blueprints
from app.routes.machines import machines_bp
from app.routes.auth import auth_bp
from app.routes.services import services_bp

# Create a list of blueprints to register in the app
blueprints = [machines_bp, services_bp, auth_bp]
