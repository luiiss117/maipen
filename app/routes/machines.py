from flask import request, render_template, redirect, url_for, session, flash, Blueprint, abort
from jinja2 import TemplateNotFound
import datetime
import app.database
import ipaddress
import uuid


t = datetime.datetime.now()
current_t = str("%s-%s-%s %s:%s" % (t.day, t.month, t.year, t.hour, t.minute))

machines_bp = Blueprint('machines', __name__, template_folder='../../templates')

@machines_bp.route('/machines', methods=['GET', 'POST'])
def my_machines():
    if session.get("user_id"):
        user_id = session.get("user_id")
        machines_list = app.database.get_machine(user_id)
        if not machines_list:
            return render_template("mymachines.html", error_no_machines_created=True)
        else:
            for name in machines_list:
                names = name[1]
    else:
        abort(401)
    return render_template("mymachines.html", machines_list=machines_list)



@machines_bp.route('/machines/add', methods=['GET', 'POST'])
def new_machine():
    if session.get("user_id"):
        if request.method == "POST":
            register_machine_name = request.form["name"]
            register_machine_ip = request.form["ip"]
            register_machine_os = request.form["os"]
            register_machine_description = request.form["description"]
            register_machine_uid = str(uuid.uuid4())
            creation_date = current_t
            update_date = current_t
            user_id = session.get("user_id")
            try:
                ipaddress.ip_address(register_machine_ip)
            except ValueError:
                return render_template("add_machine.html", ip_error=True)
            if not app.database.check_machine(user_id,register_machine_name):
                app.database.add_new_machine(user_id,register_machine_name,register_machine_ip,register_machine_os,register_machine_description,creation_date,update_date,register_machine_uid)
                flash("Machine created successfully")
                success=True
                return redirect(url_for("machines.my_machines"))
            else:
                return render_template("add_machine.html", already_exists=True)
    else:
        abort(401)
    return render_template("add_machine.html")

@machines_bp.route('/machines/<machine_uuid>', methods=['GET', 'POST'])
def machine_info(machine_uuid):
    if session.get("user_id"):
        user_id = session.get("user_id")
        m_data = app.database.get_machine_by_ids(user_id, machine_uuid)
        machine_name = m_data[1]
        machine_ip = m_data[2]
        machine_os = m_data[3]
        machine_creation_date = m_data[4]
    else:
        abort(401)
    return render_template("machine_info.html", machine_name=machine_name, machine_ip=machine_ip, machine_os=machine_os, machine_creation_date=machine_creation_date)



