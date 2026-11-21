
from models import db
from datetime import datetime


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    total_price = db.Column(db.Float, nullable=False)

    status = db.Column(db.String(50), default="Pending")

    address = db.Column(db.String(255), nullable=False)

    phone = db.Column(db.String(20), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref="orders")

    items = db.relationship(
        "OrderItem",
        backref="order",
        cascade="all, delete-orphan"
    )


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    order_id = db.Column(
        db.Integer,
        db.ForeignKey("order.id"),
        nullable=False
    )

    product_name = db.Column(db.String(150), nullable=False)

    price = db.Column(db.Float, nullable=False)

    quantity = db.Column(db.Integer, nullable=False)
