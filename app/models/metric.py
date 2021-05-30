from app import db

class Metric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    ideal_time = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<Metric %r>' % self.name
