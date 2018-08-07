from .. import db

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.String, primary_key=True)
    reminder = db.Column(db.Integer, nullable=False, default=6)

    todos = db.relationship("Todo", backref="user")
