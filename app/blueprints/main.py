from flask import Blueprint, redirect, url_for, render_template
# import pandas as pd
import mpld3
import json
from app.data import video_df

main = Blueprint('main', __name__)


# @main.route('/<uid>/')
# @main.route('/')
# def index(uid='10417ff2a789499cae7bc9a3b2517d0c'):
#     df = pd.read_sql_query('select content_url, count(*) from events group by content_url having count(*) > 50', g.db_engine)
#     return render_template('index.html', chart_data=vincent.Bar(df).to_json())


@main.route('/')
def index():
    ax = video_df.plot(x='views', y='length', kind='scatter', xlim=[video_df['views'].min(), video_df['views'].max()])
    mpld3_data = mpld3.fig_to_dict(ax.get_figure())
    return render_template('dataviz.html', data_table=video_df.head().to_html(), mpld3_data=json.dumps(mpld3_data))


@main.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='img/favicon.ico'))
