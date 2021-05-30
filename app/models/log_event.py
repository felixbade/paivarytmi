from app import db
#from app.models.metric import Metric

class LogEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    log_time = db.Column(db.DateTime, nullable=False)

    metric_id = db.Column(db.Integer, db.ForeignKey('metric.id'),
        nullable=False)
    metric = db.relationship('Metric',
        backref=db.backref('log_events', lazy=True))