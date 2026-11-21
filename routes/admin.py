
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Product, User, Order, Cart

admin = Blueprint("admin", __name__, url_prefix="/admin")


@admin.before_request
@login_required
def check_admin():
    if not current_user.is_admin:
        return redirect(url_for("main.home"))


@admin.route("/")
def dashboard():
    products = Product.query.all()
    orders_count = Order.query.count()
    users_count = User.query.count()

    return render_template(
        "admin/dashboard.html",
        products=products,
        orders_count=orders_count,
        users_count=users_count
    )


@admin.route("/products/add", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        category = request.form.get("category", "").strip()
        image = request.form.get("image", "").strip()

        try:
            price = float(request.form.get("price"))
            stock = int(request.form.get("stock"))

            if not name or not description or price < 0 or stock < 0:
                raise ValueError

            product = Product(
                name=name,
                description=description,
                price=price,
                category=category,
                stock=stock,
                image=image
            )

            db.session.add(product)
            db.session.commit()

            flash("Product added successfully!")
            return redirect(url_for("admin.dashboard"))

        except (ValueError, TypeError):
            db.session.rollback()
            flash("Please enter valid product information.")

    return render_template("admin/add_product.html")


@admin.route("/products")
def manage_products():
    products = Product.query.order_by(
        Product.created_at.desc()
    ).all()

    return render_template("admin/products.html", products=products)


@admin.route("/products/edit/<int:product_id>", methods=["GET", "POST"])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        category = request.form.get("category", "").strip()
        image = request.form.get("image", "").strip()

        try:
            price = float(request.form.get("price"))
            stock = int(request.form.get("stock"))

            if not name or not description or price < 0 or stock < 0:
                raise ValueError

            product.name = name
            product.description = description
            product.price = price
            product.category = category
            product.stock = stock
            product.image = image

            db.session.commit()

            flash("Product updated successfully!")
            return redirect(url_for("admin.manage_products"))

        except (ValueError, TypeError):
            db.session.rollback()
            flash("Please enter valid product information.")

    return render_template("admin/edit_product.html", product=product)


@admin.route("/products/delete/<int:product_id>", methods=["POST"])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)

    Cart.query.filter_by(product_id=product.id).delete()

    db.session.delete(product)
    db.session.commit()

    flash("Product deleted successfully!")
    return redirect(url_for("admin.manage_products"))


@admin.route("/orders")
def manage_orders():
    orders = Order.query.order_by(
        Order.created_at.desc()
    ).all()

    return render_template("admin/orders.html", orders=orders)


@admin.route("/users")
def manage_users():
    users = User.query.all()

    return render_template("admin/users.html", users=users)
