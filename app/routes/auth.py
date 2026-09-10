from flask import request, render_template, redirect, url_for, session, flash, Blueprint
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, HashingError, VerificationError
import app.database


auth_bp = Blueprint('auth', __name__, template_folder='../../templates')

ph = PasswordHasher()


def password_hashing(passw):
    try:
        phash = ph.hash(passw)
        return phash
    except HashingError as e:
        print("Hashing error", e)


@auth_bp.route('/login', methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("auth.dashboard"))
    else:
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            user = app.database.get_user_by_username(username)
            if not user:
                return render_template("login.html",error=True)
            try: 
                password_hash = user[2]
                ph.verify(password_hash, password)
                session["user_id"] = user[0]
                flash("Logged in successfully")
                return redirect(url_for("auth.dashboard"))
            except VerifyMismatchError:
                return render_template("login.html",error=True)
            except VerificationError:
                return "An error occurred"
            except InvalidHashError:
                return "Invalid hash"
        return render_template("login.html")

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if session.get("user_id"):
        flash("You need to logout first")
    else:
        if request.method == "POST":
            register_username = request.form["username"]
            register_passw = request.form["password"]
            user_id = session.get("user_id")

            # Check if the user exists in the database
            if not app.database.get_user_by_username(register_username):
                secured_password = password_hashing(register_passw)
                app.database.add_new_user(register_username, secured_password)
                return redirect(url_for("auth.login"))
            else:
                return render_template("register.html", error=True, register_username=register_username)
        return render_template("register.html")
    return redirect(url_for("auth.dashboard"))

@auth_bp.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if session.get("user_id"):
        user_id = session.get("user_id")
        username = app.database.get_user_by_id(user_id)[1]
    else:
        return redirect(url_for("auth.login"))
    return render_template("dashboard.html", username=username)
           
@auth_bp.route('/logout')
def logout():
        session.clear()
        return redirect("/")

@auth_bp.route('/', methods=['GET','POST'])
def index():
    return redirect(url_for("auth.login"))
