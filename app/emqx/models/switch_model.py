from app import db


class Switch(db.Model):
    __tablename__ = 'switch'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer, index=True)