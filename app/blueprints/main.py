from flask import Blueprint, redirect, url_for, render_template, g
import mpld3
import json
from .model import get_events_date_df, get_events_by_source_df
# from app.data import video_df

main = Blueprint('main', __name__)


# @main.route('/<uid>/')
# @main.route('/')
# def index(uid='10417ff2a789499cae7bc9a3b2517d0c'):
#     df = pd.read_sql_query('select content_url, count(*) from events group by content_url having count(*) > 50', g.db_engine)
#     return render_template('index.html', chart_data=vincent.Bar(df).to_json())
#
# ax = video_df.plot(x='views', y='length', kind='scatter', xlim=[video_df['views'].min(), video_df['views'].max()])
# mpld3_data = mpld3.fig_to_dict(ax.get_figure())
# return render_template('dataviz.html', data_table=video_df.head().to_html(), mpld3_data=json.dumps(mpld3_data))

@main.route('/')
def index():
    return render_template('index.html')


@main.route('/viz-date/')
def viz_date():
    df = get_events_date_df(g.db_engine)
    df = df.unstack(1)
    ax = df.plot(legend=['load', 'play'], figsize=(12, 8))
    mpld3_data = mpld3.fig_to_dict(ax.get_figure())
    return render_template('dataviz.html', data_table=df.head(25).to_html(), mpld3_data=json.dumps(mpld3_data))


@main.route('/viz-content-host/')
def viz_content_host():
    df = get_events_by_source_df(g.db_engine)
    ax = df.plot(kind='bar', figsize=(12, 8))
    mpld3_data = mpld3.fig_to_dict(ax.get_figure())
    return render_template('dataviz.html', data_table=df.head(25).to_html(), mpld3_data=json.dumps(mpld3_data))


@main.route('/tab-events/')
def tab_events():
    df = get_events_date_df(g.db_engine)
    df = df.unstack(1)
    ax = df.plot(legend=['load', 'play'])
    mpld3_data = mpld3.fig_to_dict(ax.get_figure())
    return render_template('dataviz.html', data_table=df.head(25).to_html(), mpld3_data=json.dumps(mpld3_data))


@main.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='img/favicon.ico'))
