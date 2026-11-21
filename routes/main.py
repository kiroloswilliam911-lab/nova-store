
from flask import Blueprint, render_template
from models import Product

main = Blueprint("main", __name__)


@main.route("/")
def home():
    products = Product.query.order_by(
        Product.created_at.desc()
    ).all()

    return render_template("index.html", products=products)
