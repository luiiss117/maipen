from flask import request, render_template, redirect, url_for, session, flash, Blueprint, abort
from jinja2 import TemplateNotFound
import app.database.machine
import app.database.service
from datetime import datetime, timezone
import ipaddress
import uuid


machines_bp = Blueprint('machines', __name__, template_folder='../../templates')

@machines_bp.route('/machines', methods=['GET', 'POST'])
def my_machines():
    user_id = session.get("user_id")
    if not user_id:
        abort(401)
    else:
        machines_list = app.database.machine.get_machine_by_userid(user_id)
        if not machines_list:
            return render_template("my_machines.html", error_no_machines_created=True)
        else:
            return render_template("my_machines.html", machines_list=machines_list)
    return render_template("my_machines.html", machines_list=machines_list)



@machines_bp.route('/machines/add', methods=['GET', 'POST'])
def new_machine():
    user_id = session.get("user_id")
    if not user_id:
        abort(401)
    else:
        if request.method == "POST":
            reg_m_name = request.form.get("name", "").strip()
            reg_m_ip = request.form.get("ip", "").strip()
            reg_m_os = request.form.get("os", "").strip()
            reg_m_description = request.form.get("description", "").strip()
            fields = [reg_m_name, reg_m_ip, reg_m_os]
            if any(not field for field in fields):
                error = "All fields except description are required."
                return render_template("add_machine.html", error=error)
                
            if len(reg_m_name) >= 25:
                error = "Name must be less than 25 characters."
                return render_template("add_machine.html", error=error)
            if len(reg_m_description) >= 200:
                    error = "Description must be less than 200 characters."
                    return render_template("add_machine.html", error=error)
            else:
                reg_m_uid = str(uuid.uuid4())
                t = datetime.now(timezone.utc)
                current_t = t.strftime("%Y-%m-%d %H:%M:%S")
                creation_date = current_t
                update_date = current_t
                user_id = session.get("user_id")

                try:
                    ipaddress.ip_address(reg_m_ip)
                except ValueError:
                    error = "Invalid IP Address."
                    return render_template("add_machine.html", error=error)
                
                if not app.database.machine.check_machine(user_id,reg_m_name):
                    app.database.machine.add_new_machine(user_id,reg_m_name,reg_m_ip,reg_m_os,reg_m_description,creation_date,update_date,reg_m_uid)
                    flash("Machine created successfully")
                    return redirect(url_for("machines.my_machines"))
                else:
                    error = "Machine name already exists"
                    return render_template("add_machine.html", error=error)
    return render_template("add_machine.html")

@machines_bp.route('/machines/<machine_uuid>', methods=['GET'])
def machine_info(machine_uuid):
    user_id = session.get("user_id")
    if not user_id:
        abort(401)
    machine = app.database.machine.get_machine_by_userid_and_uuid(user_id,machine_uuid)
    if not machine:
        abort(404)
    machine_id = machine[0]
    machine_name = machine[1]
    machine_ip = machine[2]
    machine_os = machine[3]
    machine_description = machine[4]
    machine_creation_date = machine[5]
    machine_uuid = machine[6]
    m_services = app.database.service.get_all_services(machine_id)
    if not m_services:
        no_services = "You don't have any services yet."
        return render_template("machine_info.html", machine_id=machine_id, machine_name=machine_name, machine_ip=machine_ip, machine_os=machine_os, machine_description=machine_description, machine_creation_date=machine_creation_date, machine_uuid=machine_uuid,no_services=no_services)
    return render_template("machine_info.html", machine_id=machine_id, machine_name=machine_name, machine_ip=machine_ip, machine_os=machine_os, machine_description=machine_description, machine_creation_date=machine_creation_date, machine_uuid=machine_uuid, m_services=m_services)

@machines_bp.route("/machines/delete/<machine_uuid>", methods=["GET", "POST"])
def machine_delete(machine_uuid):
    user_id = session.get("user_id")
    if not user_id:
        abort(401)
    if request.method == 'POST':
        confirmation = request.form.get("confirmation", "").strip()
        if confirmation != "Yes":
            return redirect(url_for("machines.my_machines")) 
        machine_id = app.database.machine.get_machineid_by_userid_and_uuid(user_id, machine_uuid)
        if not machine_id:
            flash("Machine not found")
            return redirect(url_for("machines.my_machines"))
        m_services = app.database.service.get_all_services(machine_id)
        if m_services:
            app.database.service.delete_all_services(machine_id)
        app.database.machine.delete_machine(user_id, machine_uuid)
        flash("Machine deleted successfully")
        return redirect(url_for("machines.my_machines"))
    return render_template("delete_machine.html")
