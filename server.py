from flask import Flask

from flask_login import LoginManager
from flask_migrate import Migrate
from waitress import serve

import views
import user_views
from model import Coinsurance, User, db

migrate = Migrate()
lm = LoginManager()

@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")

    app.add_url_rule("/", view_func = views.home_page)
    app.add_url_rule("/coinsurance_entry", view_func=views.coinsurance_entry, methods=["GET","POST"])
    app.add_url_rule("/coinsurance/all", view_func=views.list_coinsurance_entries, methods=['GET'])
    app.add_url_rule("/coinsurance/view/<int:coinsurance_id>", view_func=views.view_coinsurance_entry, methods=['GET','POST'])

    app.add_url_rule("/coinsurance/edit/<int:coinsurance_id>", view_func=views.edit_coinsurance_entry, methods=['GET','POST'])
    app.add_url_rule("/coinsurance/statements/<int:coinsurance_id>", view_func=views.download_statement, methods=['GET','POST'])
    app.add_url_rule("/coinsurance/confirmations/<int:coinsurance_id>", view_func=views.download_confirmation, methods=['GET','POST'])
    app.add_url_rule("/user/signup", view_func=user_views.signup, methods=["GET", "POST"])
    app.add_url_rule("/user/login", view_func=user_views.login_page, methods=["GET", "POST"])
    app.add_url_rule("/user/logout", view_func=user_views.logout_page)
    app.add_url_rule(
        "/user/reset_password",
        view_func=user_views.reset_password_page,
        methods=["GET", "POST"],
    )
    lm.init_app(app)
    lm.login_view = "login_page"

    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "postgresql://barneedhar:barneedhar@localhost:5432/coinsurance"

    db.init_app(app)
    migrate.init_app(app, db)
    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    serve(app, host="0.0.0.0", port=8080)
