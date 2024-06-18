from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Weight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    waist = db.Column(db.Float, nullable=False)
    arm = db.Column(db.Float, nullable=False)
    thigh = db.Column(db.Float, nullable=False)
    calf = db.Column(db.Float, nullable=False)
    chest = db.Column(db.Float, nullable=False)
    shoulder = db.Column(db.Float, nullable=False)
