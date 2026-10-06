from datetime import datetime

from extensions import db


class Lead(db.Model):
    __tablename__ = "leads"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    business_name = db.Column(db.String(150), nullable=True)

    email = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(30), nullable=False)

    city = db.Column(db.String(100), nullable=True)

    service = db.Column(db.String(100), nullable=False)
    budget = db.Column(db.String(50), nullable=True)

    message = db.Column(db.Text, nullable=True)

    status = db.Column(
        db.String(30),
        nullable=False,
        default="New"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):
        return f"<Lead {self.name} - {self.service}>"