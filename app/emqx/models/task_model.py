from app import db


class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    startDate = db.Column(db.String, nullable=False)
    endDate = db.Column(db.String, nullable=False)
    done = db.Column(db.Integer, index=True)