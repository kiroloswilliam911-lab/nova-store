
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Cart, Order, OrderItem

orders = Blueprint("orders", __name__)


@orders.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    items = Cart.query.filter_by(user_id=current_user.id).all()

    if not items:
        flash("Your cart is empty!")
        return redirect(url_for("cart.view_cart"))

    total = sum(
        item.product.price * item.quantity
        for item in items
    )

    if request.method == "POST":
        address = request.form.get("address", "").strip()
        phone = request.form.get("phone", "").strip()

        if not address or not phone:
            flash("Please enter your address and phone.")
            return redirect(url_for("orders.checkout"))

        # Check stock before creating the order
        for item in items:
            if item.quantity > item.product.stock:
                flash(
                    f"Not enough stock for {item.product.name}!"
                )
                return redirect(url_for("cart.view_cart"))

        # Create order
        order = Order(
            user_id=current_user.id,
            total_price=total,
            address=address,
            phone=phone
        )

        db.session.add(order)

        # Save order items
        for item in items:
            order_item = OrderItem(
                order=order,
                product_name=item.product.name,
                price=item.product.price,
                quantity=item.quantity
            )

            db.session.add(order_item)
            
        # Reduce stock and clear cart
        for item in items:
            item.product.stock -= item.quantity
            db.session.delete(item)

        db.session.commit()

        flash("Order placed successfully!")
        return redirect(url_for("orders.my_orders"))

    return render_template("checkout.html", items=items, total=total)


@orders.route("/orders")
@login_required
def my_orders():
    user_orders = Order.query.filter_by(
        user_id=current_user.id
    ).order_by(Order.created_at.desc()).all()

    return render_template("orders.html", orders=user_orders)
