from datetime import datetime
from time import strptime

from flask import render_template

from app import app, db
from app.models.metric import Metric
from app.models.log_event import LogEvent

def time_at(timestamp):
    return datetime(*(strptime(timestamp, '%H:%M')[0:6]))

@app.route('/')
def index():

    metrics = Metric.query.all()

    return render_template('frontpage.html', metrics=metrics)

@app.route('/metric/<int:metric_id>')
def view_metric(metric_id):
    metric = Metric.query.filter_by(id=metric_id).first()

    return str(metric.name)