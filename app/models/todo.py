from .. import db

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return "#"+str(self.id)+": "+self.content