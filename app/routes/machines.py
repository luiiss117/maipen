from flask import request, render_template, redirect, url_for, session, flash, Blueprint, abort
from jinja2 import TemplateNotFound
import app.database.machine
import app.database.service
import datetime
import ipaddress
import uuid


machines_bp = Blueprint('machines', __name__, template_folder='../../templates')

@machines_bp.route('/machines', methods=['GET', 'POST'])
def my_machines():
    if session.get("user_id"):
        user_id = session.get("user_id")
        machines_list = app.database.machine.get_machine_by_userid(user_id)
        if not machines_list:
            return render_template("mymachines.html", error_no_machines_created=True)
        else:
            return render_template("mymachines.html", machines_list=machines_list)
    else:
        abort(404)
    return render_template("mymachines.html", machines_list=machines_list)



@machines_bp.route('/machines/add', methods=['GET', 'POST'])
def new_machine():
    if session.get("user_id"):
        if request.method == "POST":
            register_machine_name = request.form["name"]
            if len(register_machine_name) >= 25:
                error = "Invalid name length, must be less than 25 characters."
                return render_template("add_machine.html", error=error)
            else:
                register_machine_ip = request.form["ip"]
                register_machine_os = request.form["os"]
                register_machine_description = request.form["description"]
                if len(register_machine_description) >= 200:
                    error = "Description must be less than 200 characters."
                    return render_template("add_machine.html", error=error)
                else:
                    register_machine_uid = str(uuid.uuid4())
                    t = datetime.datetime.now()
                    current_t = current_t = t.strftime("%Y-%m-%d %H:%M:%S")
                    creation_date = current_t
                    update_date = current_t
                    user_id = session.get("user_id")
                    try:
                        ipaddress.ip_address(register_machine_ip)
                    except ValueError:
                        error = "Invalid IP Address."
                        return render_template("add_machine.html", error=error)
                    if not app.database.machine.check_machine(user_id,register_machine_name):
                        app.database.machine.add_new_machine(user_id,register_machine_name,register_machine_ip,register_machine_os,register_machine_description,creation_date,update_date,register_machine_uid)
                        flash("Machine created successfully")
                        return redirect(url_for("machines.my_machines"))
                    else:
                        error = "Machine name already exists"
                        return render_template("add_machine.html", error=error)
    else:
        abort(404)
    return render_template("add_machine.html")

@machines_bp.route('/machines/<machine_uuid>', methods=['GET'])
def machine_info(machine_uuid):
    user_id = session.get("user_id")
    if user_id:
        m_data = app.database.machine.get_machine_by_userid_and_uuid(user_id,machine_uuid)
        if m_data:
            machine_id = m_data[0]
            machine_name = m_data[1]
            machine_ip = m_data[2]
            machine_os = m_data[3]
            machine_description = m_data[4]
            machine_creation_date = m_data[5]
            machine_uuid = m_data[6]
            m_services = app.database.service.get_all_services_by_id(machine_id)
        else:
            abort(404)
    else:
        abort(404)
    return render_template("machine_info.html", machine_id=machine_id, machine_name=machine_name, machine_ip=machine_ip, machine_os=machine_os, machine_description=machine_description, machine_creation_date=machine_creation_date, machine_uuid=machine_uuid, m_services=m_services)

@machines_bp.route("/machines/delete/<machine_uuid>", methods=['GET', 'POST'])
def machine_delete(machine_uuid):
    user_id = session.get("user_id")
    if user_id:
        if request.method == 'POST':
            if request.form["confirmation"] == "Yes":
                machine_id = app.database.machine.get_machineid_by_userid_and_uuid(user_id, machine_uuid)
                if machine_id:
                    app.database.service.delete_all_services(machine_id)
                    app.database.machine.delete_machine(user_id,machine_uuid)
                    flash("Machine deleted successfully")
                return redirect(url_for("machines.my_machines"))
            else:
                return redirect(url_for("machines.my_machines"))
    else:
        abort(404)
    return render_template("delete_machine.html")
