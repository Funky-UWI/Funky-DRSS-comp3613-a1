from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from flask_login import UserMixin

ACCESS = {
    "user": 1,
    "admin": 2,
}


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    access = db.Column(db.Integer, nullable=False)
    reviews = db.relationship(
        "Review", backref="user", lazy=True, cascade="all, delete-orphan"
    )

    def __init__(self, username, password, access=ACCESS["user"]):
        self.username = username
        self.set_password(password)
        self.access = access

    def is_admin(self):
        return self.access == ACCESS["admin"]

    def allowed(self, access_level):
        return self.access >= access_level

    def toJSON(self):
        return {"id": self.id, "username": self.username, "access": self.access}

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method="sha256")

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def toJSON(self):
        return {
            'id': self.id,
            'username': self.username,
            'access': self.access
        }
