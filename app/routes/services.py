from flask import request, render_template, redirect, url_for, session, flash, Blueprint, abort
from jinja2 import TemplateNotFound
import app.database.machine
import app.database.service


services_bp = Blueprint('services', __name__, template_folder='../../templates')

@services_bp.route("/machines/services/add", methods=["GET","POST"])
def new_service():
    user_id = session.get("user_id")
    if not user_id:
        abort(401)
    machine_uuid = request.args.get("m")
    if request.method == 'POST':
        machine = app.database.machine.get_machine_by_userid_and_uuid(user_id, machine_uuid)
        if not machine:
            abort(404)
        machine_id = machine[0]
        name = request.form.get("name", "").strip()
        version = request.form.get("version", "").strip()
        protocol = request.form.get("protocol", "").strip()
        port_str = request.form.get("port", "").strip()
        fields = [name, version, protocol, port_str]
        if any(not field for field in fields):
            error = "All fields are required"
            return render_template("add_service.html", error=error, machine_uuid=machine_uuid)
        protocols = ["TCP", "UDP", "TCP&UDP"]
        if not protocol in protocols:
            error = "Invalid protocol"
            return render_template("add_service.html", error=error, machine_uuid=machine_uuid)
        try:
            port = int(port_str)
        except ValueError:
            error = "Port must be a number"
            return render_template("add_service.html", error=error, machine_uuid=machine_uuid)
        if port > 65535 or port < 1:
            error = "Invalid port number"
            return render_template("add_service.html", error=error, machine_uuid=machine_uuid)
        if app.database.service.get_service_port(machine_id,port):
            error = "Port already exist"
            return render_template("add_service.html", error=error, machine_uuid=machine_uuid)
        if len(name) >= 25:
            error = "Name must be less than 25 characters."
            return render_template("add_service.html", error=error, machine_uuid=machine_uuid)
        if len(version) >= 30:
            error = "Version must be less than 30 characters"
            return render_template("add_service.html", error=error, machine_uuid=machine_uuid)
        app.database.service.add_new_service(protocol,port,name,version,machine_id)
        flash("Service added successfully")
        return render_template("add_service.html", machine_uuid=machine_uuid)
    return render_template("add_service.html", machine_uuid=machine_uuid)


@services_bp.route("/machines/services/delete", methods=["GET", "POST"])
def delete_service():
    user_id = session.get("user_id")
    if not user_id:
        abort(401)
    machine_uuid = request.args.get("m")    
    if request.method == "POST":
        machine = app.database.machine.get_machine_by_userid_and_uuid(user_id, machine_uuid)
        if not machine:
            abort(404)
        machine_id = machine[0]
        port_str = request.args.get("p")
        try:
            port = int(port_str)
        except ValueError:
            flash("Error: Port must be a number!")
            return redirect(url_for("machines.machine_info", machine_uuid=machine_uuid))
        confirmation = request.form.get("confirmation", "").strip()
        if not app.database.service.get_service_id(machine_id,port):
            flash("Error: This service doesn't exist")
            return redirect(url_for("machines.machine_info", machine_uuid=machine_uuid))
        if confirmation != "Yes":
            return redirect(url_for("machines.machine_info", machine_uuid=machine_uuid))
        app.database.service.delete_service(machine_id,port)
        flash("Service deleted successfully")
        return redirect(url_for("machines.machine_info", machine_uuid=machine_uuid))
    return render_template("delete_service.html",machine_uuid=machine_uuid)
