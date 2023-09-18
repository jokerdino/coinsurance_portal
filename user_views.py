from form import SignupForm, LoginForm
from flask import flash, redirect, render_template, request, send_file, url_for
from model import User
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import or_, select


def signup():
    from server import db

    form = SignupForm()

    #    if request.method == "GET":
    #        return render_template("signup.html", form=form)
    if request.method == "POST":
        username = form.data["username"]
        password = form.data["password"]
        password_hash = generate_password_hash(password, method="sha256")

        #emp_number = form.data["emp_number"]

        user = User.query.filter(
            or_(User.username == username)#, User.emp_number == emp_number)
        ).first()
        if user:
            flash("Username or employee number already exists.")
            # return redirect(url_for("signup"))

        else:
            # add employee number to employee database if employee number does not exist
          #  employee = Employee.query.filter(Employee.emp_number == emp_number).first()
           # if not employee:
            #    print("employee number does not exist")
             #   new_employee = Employee(name=username, emp_number=emp_number)
              #  db.session.add(new_employee)
            user = User(
                username=username, password=password_hash)#, emp_number=emp_number
            #)
            db.session.add(user)
            #user_views.admin_check()
            db.session.commit()

            return redirect(url_for("login_page"))
    return render_template("signup.html", form=form)


def login_page():
    if current_user.is_authenticated:
        return redirect(url_for("home_page"))
    form = LoginForm()

    from server import db

    if form.validate_on_submit():
        username = form.data["username"]
        user = db.session.query(User).filter(User.username == username).first()
        if user is not None:
            password = form.data["password"]

            if check_password_hash(user.password, password):
                login_user(user)

                next_page = request.args.get("next", url_for("home_page"))
                return redirect(next_page)
            else:
                flash("Invalid credentials.")
        else:
            flash("Invalid credentials.")
    return render_template("login.html", form=form)


def logout_page():
    logout_user()
    # flash("You have logged out.")
    return redirect(url_for("home_page"))

def reset_password_page():
    #    pass
    form = ResetPasswordForm()
    from server import db

    #  form = SignupForm()
    if request.method == "GET":
        return render_template("reset_password.html", form=form)
    else:
        username = form.data["username"]
        emp_number = form.data["emp_number"]

        user = User.query.filter(
            User.username == username, User.emp_number == emp_number
        ).first()
        if user:
            if user.reset_password_page:
                password = form.data["password"]
                password_hash = generate_password_hash(password, method="sha256")
                user.password = password_hash
                user.reset_password_page = False
                db.session.add(user)
                db.session.commit()
                return redirect(url_for("login_page"))
            else:
                flash(
                    "Password reset page is not enabled for this user. Contact admin."
                )
            # return redirect(url_for("signup"))

        else:
            flash("Username or employee number does not exist.")
    return render_template("reset_password.html", form=form)
