
from flask import Blueprint, render_template
from models import Product

products = Blueprint("products", __name__)


@products.route("/products")
def all_products():
    items = Product.query.order_by(
        Product.created_at.desc()
    ).all()

    return render_template("products.html", products=items)


@products.route("/product/<int:product_id>")
def product_details(product_id):
    product = Product.query.get_or_404(product_id)

    return render_template(
        "product_details.html",
        product=product
    )
