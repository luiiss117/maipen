from flask import request, render_template, redirect, url_for, session, flash, Blueprint, abort
from jinja2 import TemplateNotFound
import app.database.machine
import app.database.service


services_bp = Blueprint('services', __name__, template_folder='../../templates')

@services_bp.route("/machines/services/add", methods=["GET","POST"])
def new_service():
    user_id = session.get("user_id")
    if user_id:
        machine_uuid = request.args.get("m")
        if request.method == 'POST':
            machine_id = app.database.machine.get_machine_by_userid_and_uuid(user_id, machine_uuid)[0]
            if not machine:
            abort(404)
            else:
                try:
                    port = int(request.form["port"])
                    if port > 65535 or port < 1:
                        error="Invalid port number"
                        return render_template("add_service.html", error=error)
                except ValueError:
                    error="Port must be a number"
                    return render_template("add_service.html", error=error)
                if app.database.service.get_service_port(machine_id,port):
                    error="Invalid port number"
                    return render_template("add_service.html", error=error)
                else:
                    name = request.form["name"]
                    version = request.form["version"]
                    protocol = request.form["protocol"]
                    app.database.service.add_new_service(protocol,port,name,version,machine_id)
                    flash("Service added successfully")
            return render_template("add_service.html")
    else:
        abort(404)
        return render_template("add_service.html")
    return render_template("add_service.html", machine_uuid=machine_uuid)


@services_bp.route("/machines/services/delete", methods=["GET","POST"])
def delete_service():
    user_id = session.get("user_id")
    if user_id:
        machine_uuid = request.args.get("m")
        if request.method == "POST":
            machine_id = app.database.machine.get_machine_by_userid_and_uuid(user_id, machine_uuid)[0]
            port = request.args.get("p")
            if app.database.service.get_service_id(machine_id,port):
                if request.form["confirmation"] == "Yes":
                    app.database.service.delete_service(machine_id,port)
                    flash("Service deleted successfully")
                    return redirect(url_for("machines.machine_info", machine_uuid=machine_uuid))
                else:
                    return redirect(url_for("machines.machine_info", machine_uuid=machine_uuid))
            else:
                flash("This service doesn't exist")
                return redirect(url_for("machines.machine_info", machine_uuid=machine_uuid))
            return render_template("delete_service.html")
    else:
        abort(404)
    return render_template("delete_service.html",machine_uuid=machine_uuid)
