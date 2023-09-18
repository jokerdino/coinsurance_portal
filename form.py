from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, IntegerField, BooleanField, SelectField, DateField

from wtforms.validators import DataRequired, NumberRange, Optional

class CoinsuranceForm(FlaskForm):
    coinsurer_list = ['SBI General', 'Royal Sundaram']

    regional_office_code = IntegerField("Enter Regional Office Code:")
    oo_code = IntegerField("Enter operating office code:")
    coinsurer_name = SelectField("Enter coinsurer name:", choices=coinsurer_list)
    coinsurer_office_code = IntegerField("Enter Coinsurer office code:")
    type_of_transaction = SelectField("Select whether leader or follower:", choices=["Leader", "Follower"])
    request_id = StringField("Enter Request ID")
    statement = FileField("Upload statement")
    confirmation = FileField("Upload confirmation")
    payable_amount = IntegerField("Enter payable amount:")
    receivable_amount = IntegerField("Enter receivable amount:")
    current_status = SelectField("Current status:", choices=coinsurer_list)
    date_of_settlement = DateField("Date of settlement:")
    amount_settled = IntegerField("Amount settled")
    utr_number = StringField("UTR number:")

class SignupForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    emp_number = IntegerField(
        "Employee number",
        validators=[NumberRange(min=10000, max=99999), DataRequired()],
    )


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])


class UpdateUserForm(FlaskForm):
    is_admin = BooleanField("Make the user admin: ")
    reset_password_page = BooleanField("Enable password reset page: ")


class ResetPasswordForm(FlaskForm):
    username = StringField("Enter username:", validators=[DataRequired()])
    emp_number = IntegerField("Enter employee number: ", validators=[DataRequired()])
    #  reset_code = IntegerField("Enter reset code received from admin: ", validators=[DataRequired()])
    password = PasswordField("Enter new password: ", validators=[DataRequired()])
