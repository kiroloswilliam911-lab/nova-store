from flask import Blueprint, redirect, url_for, flash, render_template
from flask_login import login_required, current_user
from models import db, Cart, Product

cart = Blueprint("cart", __name__)


@cart.route("/cart/add/<int:product_id>", methods=["POST"])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)

    item = Cart.query.filter_by(
        user_id=current_user.id,
        product_id=product.id
    ).first()

    if product.stock <= 0:
        flash("This product is out of stock!")
        return redirect(url_for("products.product_details", product_id=product.id))

    if item:
        if item.quantity >= product.stock:
            flash("Not enough stock available!")
            return redirect(url_for("products.product_details", product_id=product.id))

        item.quantity += 1
    else:
        item = Cart(
            user_id=current_user.id,
            product_id=product.id,
            quantity=1
        )
        db.session.add(item)

    db.session.commit()
    flash("Product added to cart!")

    return redirect(url_for("cart.view_cart"))


@cart.route("/cart/remove/<int:item_id>", methods=["POST"])
@login_required
def remove_from_cart(item_id):
    item = Cart.query.filter_by(
        id=item_id,
        user_id=current_user.id
    ).first_or_404()

    db.session.delete(item)
    db.session.commit()

    flash("Product removed from cart!")

    return redirect(url_for("cart.view_cart"))

@cart.route("/cart")
@login_required
def view_cart():
    items = Cart.query.filter_by(user_id=current_user.id).all()

    total = sum(
        item.product.price * item.quantity
        for item in items
    )

    return render_template("cart.html", items=items, total=total)