from flask import request, render_template, redirect, url_for, session, flash, Blueprint, abort
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, HashingError, VerificationError, InvalidHashError
import app.database.user


auth_bp = Blueprint('auth', __name__, template_folder='../../templates')

ph = PasswordHasher()


def password_hashing(passw):
    try:
        phash = ph.hash(passw)
        return phash
    except HashingError as e:
        print("Hashing error:", e)


@auth_bp.route('/login', methods=["GET", "POST"])
def login():
    user_id = session.get("user_id")
    if user_id:
        return redirect(url_for("auth.dashboard"))
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if not username or not password:
            error = "All fields are required"
            return render_template("login.html", error=error)
        user = app.database.user.get_user_by_username(username)
        if not user:
            error = "Invalid credentials"
            return render_template("login.html", error=error)
        try: 
            password_hash = user[2]
            ph.verify(password_hash, password)
            session["user_id"] = user[0]
            flash("Logged in successfully")
            return redirect(url_for("auth.dashboard"))
        except VerifyMismatchError:
            error = "Invalid credentials"
            return render_template("login.html",error=error)
        except VerificationError:
            error = "A verification error occurred"
            return render_template("login.html", error=error)
        except InvalidHashError:
            error = "Hash error"
            return render_template("login.html", error=error)
    return render_template("login.html")

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    user_id = session.get("user_id")
    if user_id:
        flash("Error: You need to logout first")
        return redirect(url_for("auth.dashboard"))
    if request.method == "POST":
        register_username = request.form.get("username", "").strip()
        register_passw = request.form.get("password", "")
        if not register_username or not register_passw:
            error = "All fields are required."
            return render_template("register.html", error=error)
        # Check if the user exists in the database
        if app.database.user.get_user_by_username(register_username):
            error = "This username already exists."
            return render_template("register.html", error=error)
        secured_password = password_hashing(register_passw)
        app.database.user.add_new_user(register_username, secured_password)
        return redirect(url_for("auth.login"))
    return render_template("register.html")

@auth_bp.route('/dashboard', methods=['GET'])
def dashboard():
    user_id = session.get("user_id")
    if not user_id:
        abort(401)
    user = app.database.user.get_user_by_id(user_id)
    if not user:
        session.pop("user_id", None)
        flash("This user doesn't exists")
        return redirect(url_for("auth.register"))
    username = user[1]
    return render_template("dashboard.html", username=username)
           
@auth_bp.route('/logout')
def logout():
        session.clear()
        return redirect(url_for("auth.login"))

@auth_bp.route('/')
def index():
    return redirect(url_for("auth.login"))

@auth_bp.route('/user/delete', methods=["GET", "POST"])
def delete_account():
    user_id = session.get("user_id")
    if not user_id:
        abort(401)
    if request.method == "POST":
        confirmation = request.form.get("confirmation", "").strip()
        if confirmation != "Yes":
            return redirect(url_for("auth.dashboard"))
        machines = app.database.machine.get_machine_by_userid(user_id)
        if machines:
            for machine in machines:
                machine_id = machine[0]
                app.database.service.delete_all_services(machine_id)
            app.database.machine.delete_all_machines_by_userid(user_id)
        app.database.user.delete_account(user_id)
        session.clear()
        flash("Account deleted successfully")
        return redirect(url_for("auth.register"))
    return render_template("delete_account.html")
