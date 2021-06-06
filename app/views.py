from datetime import datetime, timedelta
from time import strptime
from math import ceil

from flask import render_template, request, redirect

from app import app, db
from app.models.metric import Metric
from app.models.log_event import LogEvent



# Helpers

def time_at(timestamp):
    return datetime(*(strptime(timestamp, '%H:%M')[0:6]))

def date_from_weeknumber_day(year, weeknumber, weekday):
    if weekday == 0:
        # todo bug with weeknumber=1
        weekday = 7
        weeknumber -= 1
    return datetime.fromisocalendar(year, weeknumber, weekday)

def get_metrics():
    return Metric.query.order_by(Metric.ideal_time.asc()).all()

def get_log_event_at(metric, year, weeknumber, weekday):
    events = LogEvent.query.filter(LogEvent.date == date_from_weeknumber_day(year, weeknumber, weekday), LogEvent.metric_id == metric.id)
    event = events.order_by(LogEvent.id.desc()).first()

    success = 1
    if event:
        diff = (event.log_time - metric.ideal_time)
        if diff < timedelta(hours=-12):
            diff += timedelta(days=1)
        if diff.days == 0:
            hour_diff = diff.seconds / 60 / 60
            success = int(ceil(min(hour_diff / 1.5 + 1, 5)))

    if not event:
        return None
    else:
        return {
            'time': event.log_time.strftime('%H:%M'),
            'success': success
        }

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
                'log_event': get_log_event_at(metric, year, weeknumber, weekday)
            }
            for weekday in range(7)
        ]
    }




# Metric list

@app.route('/')
def index():
    metrics = get_metrics()
    return render_template('frontpage.html', metrics=metrics)



# Weeks in a metric

@app.route('/metric/<int:metric_id>/')
def view_metric(metric_id):
    metric = Metric.query.filter_by(id=metric_id).first()
    year, weeknumber, weekday = datetime.now().isocalendar()
    if weekday == 7:
        # todo bug with weeknumber=1
        weekday = 0
        weeknumber += 1
    weeks = []
    weeks.append(get_week_data(metric, (year, weeknumber-1)))
    weeks.append(get_week_data(metric, (year, weeknumber)))

    return render_template('metric.html', metric=metric, weeks=weeks)



# Metrics in week

@app.route('/week')
def view_week():
    current_year, current_weeknumber, _ = datetime.now().isocalendar()
    
    year = int(request.args.get('year', current_year))
    weeknumber = int(request.args.get('weeknumber', current_weeknumber))

    week = {
        'year': year,
        'weeknumber': weeknumber
    }

    metrics = []
    for metric in get_metrics():
        metrics.append(get_week_data(metric, (year, weeknumber)))

    return render_template('week.html', week=week, metrics=metrics)



# Add/edit datapoint

@app.route('/edit')
def edit_log_data():
    params = {}
    params['year'] = int(request.args.get('year'))
    params['weeknumber'] = int(request.args.get('weeknumber'))
    params['weekday'] = int(request.args.get('weekday'))

    metric_id = request.args.get('metric_id')
    params['metric'] = Metric.query.filter_by(id=metric_id).first()

    params['return_to'] = request.referrer

    return render_template('log_event.html', **params)

@app.route('/edit', methods=['POST'])
def submit_log_data():
    year = int(request.form.get('year'))
    weeknumber = int(request.form.get('weeknumber'))
    weekday = int(request.form.get('weekday'))
    d = date_from_weeknumber_day(year, weeknumber, weekday)

    log_time = time_at(request.form.get('timestamp'))

    metric_id = int(request.form.get('metric_id'))

    db.session.add(LogEvent(date=d, log_time=log_time, metric_id=metric_id))
    db.session.commit()
    
    return redirect(request.form.get('return_to'))