import os

from flask import Flask
from flask_login import LoginManager
from config import Config
from models import db, User

from routes.main import main
from routes.auth import auth
from routes.products import products
from routes.cart import cart
from routes.orders import orders
from routes.admin import admin


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


app.register_blueprint(main)
app.register_blueprint(auth)
app.register_blueprint(products)
app.register_blueprint(cart)
app.register_blueprint(orders)
app.register_blueprint(admin)


with app.app_context():
    db.create_all()

admin_email = os.environ.get("ADMIN_EMAIL")
admin_password = os.environ.get("ADMIN_PASSWORD")

if admin_email and admin_password:
    admin_user = User.query.filter_by(email=admin_email).first()

    if not admin_user:
        admin_user = User(
            username="Admin",
            email=admin_email,
            is_admin=True
        )
        admin_user.set_password(admin_password)
        db.session.add(admin_user)
        db.session.commit()


if __name__ == "__main__":
    app.run(debug=True)