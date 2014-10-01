from flask import Blueprint, redirect, url_for, request, render_template, g
import mpld3
import seaborn  # imported for Styling matplotlib plots
import json
from .model import get_events_date_df, get_events_by_source_df, get_events_by_content
# from app.data import video_df

main = Blueprint('main', __name__)


def get_params(request=request):
    params = {}
    params['client'] = request.args.get('client', 'storify.com')
    params['from_date'] = request.args.get('from-date', '2014-09-20')
    params['to_date'] = request.args.get('to-date', '2014-09-26')
    params['content_host'] = request.args.get('content-host', '')
    if not params['content_host']:
        for idx, host in enumerate(get_content_hosts()):
            params['content_host' + str(idx + 1)] = host
    else:
        for idx in range(1, 5):
            params['content_host' + str(idx)] = params['content_host']
    return params


def get_content_hosts():
    hosts = []
    for host in ['instagram.com', 'vine.co', 'youtube.com', 'youtu.be']:
        hosts.append(host)
    return hosts


def get_clients():
    clients = []
    for client in ['2dayfm.com.au', 'change.org', 'conservativetribune.com', \
                'disqus.com', 'edmodo.com', 'fox-sports.massrel.io', 'gamespot.com', \
                'genius.com', 'giantbomb.com', 'indiegogo.com', 'knowyourmeme.com', \
                'lockerdome.com', 'medium.com', 'moviepilot.com', 'rap.genius.com', \
                'redditmedia.com', 'storify.com', 'thescore.com', 'thrillon.com', \
                'up.massrelevance.com', 'vulture.com']:
        clients.append(client)
    return clients


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/slides/')
def slides():
    return render_template('slides.html')


@main.route('/viz-date/')
def viz_date():
    params = get_params(request)
    df = get_events_date_df(g.db_engine, params)
    df = df.unstack(1)
    ax = df.plot(legend=['load', 'play'], figsize=(12, 8))
    ax.set_xlabel('Date')
    mpld3_data = mpld3.fig_to_dict(ax.get_figure())
    table_df = get_events_by_source_df(g.db_engine, params)
    ratio_format = lambda x: '<span class="significant"><bold>%f</bold></span>' % x
    table_html = table_df.head(20).to_html(classes=['table'], formatters={'ratio': ratio_format})
    return render_template('base_viz.html', \
        clients=get_clients(), content_hosts=get_content_hosts(), params=params, \
        data_table=table_html, mpld3_data=json.dumps(mpld3_data))


@main.route('/viz-content/')
def viz_content():
    params = get_params(request)
    df = get_events_by_content(g.db_engine, params)
    ax = df.plot(x='loaded', y='played', kind='scatter', figsize=(12, 8))
    mpld3_data = mpld3.fig_to_dict(ax.get_figure())
    url_format = lambda x: '<a href="%s">%s</a>' % (x, x)
    table_html = df.head(20).to_html(classes=['table'], formatters={'content_url': url_format})
    return render_template('base_viz.html', \
        clients=get_clients(), content_hosts=get_content_hosts(), params=params, \
        data_table=table_html, mpld3_data=json.dumps(mpld3_data))


@main.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='img/favicon.ico'))
