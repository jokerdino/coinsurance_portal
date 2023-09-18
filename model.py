from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)


db = SQLAlchemy(metadata=metadata)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    user_type  = db.Column(db.String)
    reset_password = db.Column(db.Boolean)

    @property
    def is_active(self):
        return True

    def is_authenticated(self):
        return True

class Coinsurance(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    uiic_regional_code = db.Column(db.Integer)
    uiic_office_code = db.Column(db.Integer)
    follower_company_name = db.Column(db.String)
    follower_office_code = db.Column(db.Integer)
    type_of_transaction = db.Column(db.String)
    request_id = db.Column(db.String)
    payable_amount = db.Column(db.Integer)
    receivable_amount = db.Column(db.Integer)
    net_amount = db.Column(db.Integer)
    statement = db.Column(db.String)
    confirmation = db.Column(db.String)
    current_status = db.Column(db.String)
    remarks = db.Column(db.String)
    date_of_settlement = db.Column(db.Date)
    settled_amount = db.Column(db.Integer)
    utr_number = db.Column(db.String)
