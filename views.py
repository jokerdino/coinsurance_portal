from datetime import datetime
from flask import flash, redirect, render_template, request, send_file, send_from_directory, url_for
import os
from form import CoinsuranceForm
from werkzeug.utils import secure_filename

from flask_login import current_user, login_required, login_user, logout_user

from model import Coinsurance, User

def home_page():
    return render_template("home.html")

def coinsurance_entry():
    from server import db
    form = CoinsuranceForm()
    if form.validate_on_submit():
        print(request.form.to_dict())
        regional_office_code = form.data['regional_office_code']
        oo_code = form.data['oo_code']
        coinsurer_name = form.data['coinsurer_name']
        coinsurer_office_code = form.data['coinsurer_office_code']
        payable_amount = form.data['payable_amount']
        receivable_amount = form.data['receivable_amount']
        #statement_filename = str(coinsurer_name) + str(oo_code) + "statement"
        statement_filename_data = secure_filename(form.data['statement'].filename)
        #print(statement)
        statement_file_extension = statement_filename_data.rsplit('.', 1)[1]
        #print(file_extension)
        statement_filename =  "statement" + datetime.now().strftime("%d%m%Y %H%M%S") + "." + statement_file_extension
        form.statement.data.save('statements/' + statement_filename)

        confirmation_filename_data = secure_filename(form.data['confirmation'].filename)
        #confirmation_filename = str(coinsurer_name) + str(oo_code) + "confirmation"
        confirmation_file_extension = confirmation_filename_data.rsplit('.', 1)[1]
        confirmation_filename =  "confirmation" + datetime.now().strftime("%d%m%Y %H%M%S") + "." + confirmation_file_extension
        #request.files['confirmation']#secure_filename(form.data['confirmation'])
        form.confirmation.data.save('confirmations/' + confirmation_filename)
        current_status = form.data['current_status']
        coinsurance = Coinsurance(uiic_regional_code=regional_office_code, uiic_office_code=oo_code,
                follower_company_name=coinsurer_name,follower_office_code=coinsurer_office_code,
                payable_amount = payable_amount, receivable_amount = receivable_amount,
                current_status = current_status, statement=statement_filename, confirmation = confirmation_filename)
        db.session.add(coinsurance)
        db.session.commit()
    return render_template("coinsurance_entry.html", form=form)

def view_coinsurance_entry(coinsurance_id):
    coinsurance = Coinsurance.query.get_or_404(coinsurance_id)
    return render_template("view_coinsurance_entry.html", coinsurance = coinsurance)

def download_statement(coinsurance_id):
    coinsurance = Coinsurance.query.get_or_404(coinsurance_id)
    statement_filename = f"{coinsurance.type_of_transaction} statement - {coinsurance.uiic_office_code} - {coinsurance.follower_company_name} {coinsurance.net_amount}"
    return send_from_directory(directory='statements/', path= coinsurance.statement, as_attachment=True, download_name=statement_filename)

def download_confirmation(coinsurance_id):
    coinsurance = Coinsurance.query.get_or_404(coinsurance_id)
    confirmation_filename = f"{coinsurance.type_of_transaction} confirmation - {coinsurance.uiic_office_code} - {coinsurance.follower_company_name} {coinsurance.net_amount}"
    return send_from_directory(directory='confirmations/', path= coinsurance.confirmation, as_attachment=True, download_name = confirmation_filename)

def edit_coinsurance_entry(coinsurance_id):
    from server import db
    form = CoinsuranceForm()
    coinsurance = Coinsurance.query.get_or_404(coinsurance_id)

    if form.validate_on_submit():
        regional_office_code = form.data['regional_office_code']
        oo_code = form.data['oo_code']
        coinsurer_name = form.data['coinsurer_name']
        coinsurer_office_code = form.data['coinsurer_office_code']
        payable_amount = form.data['payable_amount']
        receivable_amount = form.data['receivable_amount']
        coinsurance.uiic_regional_code = regional_office_code
        coinsurance.uiic_office_code = oo_code

        db.session.commit()
    form.regional_office_code.data = coinsurance.uiic_regional_code
    form.oo_code.data = coinsurance.uiic_office_code
    return render_template("coinsurance_entry.html", form = form, coinsurance = coinsurance)


def list_coinsurance_entries():
    from server import db

    coinsurance_entries = Coinsurance.query.all()
    return render_template("coinsurance_entries_all.html", coinsurance_entries = coinsurance_entries)
