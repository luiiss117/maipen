from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask_session import Session
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from os import environ
from dotenv import load_dotenv
import database



app = Flask(__name__)

load_dotenv()
app.secret_key = environ["SECRET_KEY"] # Secret key for Session
app.config["SESSION_PERMANENT"] = False     # Sessions expire when the browser is closed
app.config["SESSION_TYPE"] = "filesystem"     # Store session data in files

Session(app)

def password_hashing(passw):
    ph = PasswordHasher()
    phash = ph.hash(passw)
    is_valid = ph.verify(phash, passw)
    needs_rehash = ph.check_needs_rehash(phash)
    return phash

# Create a function called home, that path is / and automatically redirects to /login
@app.route('/login', methods=["GET", "POST"])
def login():
    ph = PasswordHasher()
    if request.method == "POST":
        user = request.form["username"]
        passw = request.form["password"]
        try:
            if database.check_user(user) == True:
                password_hash = database.check_passw(user)
                ph.verify(password_hash, passw)
                session["name"] = user
                # Create a session for the correct user and then redirect to /dashboard (dashboard will contain the username and his machines in the page, at first, need access control regulations)
                flash("Logged in successfully")
                return redirect(url_for("dashboard"))
        except VerifyMismatchError:
                return "Invalid credentials"
        else:
            return "Invalid credentials"
    return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        register_username = request.form["username"]
        register_passw = request.form["password"]
        secured_password = password_hashing(register_passw)

        # Check if the user exists in the database
        if database.is_username_taken(register_username) == False:    
            database.add_new_user(register_username, secured_password)
            return redirect(url_for("login"))
        else:
            return render_template("register.html", error=True, register_username=register_username)
    return render_template("register.html")

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if not session.get("name"):
        return redirect(url_for("login")) 
    
    return render_template("dashboard.html", username=session["name"])
           
@app.route('/logout')
def logout():
        session["name"] = None
        return redirect("/")

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == "POST":
        return redirect(url_for("login"))
    return redirect(url_for("login"))

if __name__ == '__main__':
    database.init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
    

