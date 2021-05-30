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

def get_week_data(metric, week):
    year, weeknumber = week
    return {
        'week': {
            'year': year,
            'weeknumber': weeknumber
        },
        'metric': metric,
        'days': [
            {
                'weekday': weekday,
                'log_event': {
                    'time': '20:30',
                    'success': weekday
                } if weekday in [1, 2, 3, 4, 5] else None
            }
            for weekday in range(7)
        ]
    }

@app.route('/metric/<int:metric_id>')
def view_metric(metric_id):
    metric = Metric.query.filter_by(id=metric_id).first()
    year, weeknumber, weekday = datetime.now().isocalendar()
    weeks = []
    weeks.append(get_week_data(metric, (year, weeknumber-1)))
    weeks.append(get_week_data(metric, (year, weeknumber)))

    return render_template('metric.html', metric_name=metric.name, weeks=weeks)

