from flask import current_app as app
from flask import redirect, render_template, url_for, request, flash

from .forms import *
from .Login import *
from .Reservation import *

@app.route("/", methods=['GET', 'POST'])
def user_options():
    
    form = UserOptionForm()
    if request.method == 'POST' and form.validate_on_submit():
        option = request.form['option']

        if option == "1":
            return redirect('/admin')
        else:
            return redirect("/reservations")
    
    return render_template("options.html", form=form, template="form-template")

@app.route("/admin", methods=['GET', 'POST'])
def admin():

    form = AdminLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']
        try:
            login = Login(username, password)
        except Exception as ex:
            error = ex
        else:
            if login.isLoggedIn:
                error = None
                login_success = True
                try:
                    reservations = Reservation()
                except Exception as ex:
                    error = ex
                else:
                    seating_chart = reservations.bus_map
                    total_sales = f"{reservations.calculate_total_sales():.2f}"
                    return render_template("admin.html", form=form, template="form-template", error=error, login_success=login_success, seating_chart=seating_chart, total_sales=total_sales)
            else:
                error = "Error!: Bad Username or Password...  Please try again...."
                login_success = False
            return render_template("admin.html", form=form, template="form-template", error=error, login_success=login_success)
        return render_template("admin.html", form=form, template="form-template", error=error)
    return render_template("admin.html", form=form, template="form-template")

@app.route("/reservations", methods=['GET', 'POST'])
def reservations():

    form = ReservationForm()
    if request.method == 'POST' and form.validate_on_submit():
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        row = request.form['row']
        seat = request.form['seat']
        try:
            reservations = Reservation()
        except Exception as ex:
            error = ex
        else:
            try:
                reservation_msg = reservations.make_reservation(first_name, last_name, int(row), int(seat))
            except Exception as ex:
                error = ex
            else:
                e_ticket = reservations.e_ticket
                form.seating_chart = reservations.bus_map
                return render_template("reservations.html", form=form, template="form-template", reservation_msg=reservation_msg, e_ticket=e_ticket)
        return render_template("reservations.html", form=form, template="form-template", error=error)
    return render_template("reservations.html", form=form, template="form-template")


