
from models import db
from datetime import datetime


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(150), nullable=False)

    description = db.Column(db.Text, nullable=False)

    price = db.Column(db.Float, nullable=False)

    image = db.Column(db.String(255))

    category = db.Column(db.String(100))

    stock = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.CheckConstraint("price >= 0", name="check_product_price"),
        db.CheckConstraint("stock >= 0", name="check_product_stock"),
    )
