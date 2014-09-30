from flask import Blueprint, redirect, url_for, request, render_template, g
import mpld3
import seaborn as sns
import json
from .model import get_events_date_df, get_events_by_source_df
# from app.data import video_df

main = Blueprint('main', __name__)


def get_params(request=request):
    params = {}
    params['client'] = request.args.get('client', 'storify.com')
    params['from_date'] = request.args.get('from-date', '09/20/2014')
    params['to_date'] = request.args.get('to-date', '09/26/2014')
    return params


@main.route('/')
def index():
    params = get_params()
    return render_template('index.html', params=params)


@main.route('/slides/')
def slides():
    params = get_params()
    return render_template('slides.html', params=params)


@main.route('/viz-date/')
def viz_date():
    params = get_params(request)
    df = get_events_date_df(g.db_engine, params)
    df = df.unstack(1)
    ax = df.plot(legend=['load', 'play'], figsize=(12, 8))
    mpld3_data = mpld3.fig_to_dict(ax.get_figure())
    return render_template('dataviz.html', params=params, data_table=df.head(25).to_html(), mpld3_data=json.dumps(mpld3_data))


@main.route('/viz-content-host/')
def viz_content_host():
    params = get_params(request)
    df = get_events_by_source_df(g.db_engine, params)
    ax = df.plot(kind='bar', figsize=(12, 8))
    mpld3_data = mpld3.fig_to_dict(ax.get_figure())
    return render_template('dataviz.html', params=params, data_table=df.head(25).to_html(), mpld3_data=json.dumps(mpld3_data))


@main.route('/tab-events/')
def tab_events():
    params = get_params(request)
    df = get_events_date_df(g.db_engine, params=params)
    df = df.unstack(1)
    ax = df.plot(legend=['load', 'play'])
    mpld3_data = mpld3.fig_to_dict(ax.get_figure())
    return render_template('dataviz.html', params=params, data_table=df.head(25).to_html(), mpld3_data=json.dumps(mpld3_data))


@main.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='img/favicon.ico'))
