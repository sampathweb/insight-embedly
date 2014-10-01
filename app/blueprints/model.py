import pandas as pd


def get_events_date_df(db_engine, params):
    events_bydate_df = pd.read_sql('''select ev_date, activity, sum(act_count) as act_count
                             from events
                             where client_host = %(client_host)s
                                and ( content_host = %(content_host1)s or
                                     content_host = %(content_host2)s or
                                     content_host = %(content_host3)s or
                                     content_host = %(content_host4)s )
                                and ( activity = %(activity1)s or
                                    activity = %(activity2)s )
                                and ( ev_date between %(ev_date1)s and %(ev_date2)s )
                             group by ev_date, activity
                             having sum(act_count) > 100
                             order by ev_date, activity

                            ''', \
        db_engine, \
        params={'client_host': params['client'],
            'content_host1': "instagram.com",
            'content_host2': "youtube.com",
            'content_host3': "youtu.be",
            'content_host4': "vine.co",
            'activity1': 'load',
            'activity2': 'play',
            'ev_date1': params['from_date'],
            'ev_date2': params['to_date']},
        index_col=['ev_date', 'activity'])
    return events_bydate_df


def get_events_by_source_df(db_engine, params):
    events_bycontent_load_df = pd.read_sql('''select ev_date, content_host, sum(act_count) as loaded
                           from events
                           where client_host = %(client_host)s
                             and ( content_host = %(content_host1)s or
                                   content_host = %(content_host2)s or
                                   content_host = %(content_host3)s or
                                   content_host = %(content_host4)s )
                            and activity = %(activity1)s
                            and ( ev_date between %(ev_date1)s and %(ev_date2)s )
                           group by ev_date, content_host
                           order by ev_date, content_host
                    ''', \
                    db_engine, \
                    params={'client_host': params['client'],
                            'content_host1': "instagram.com",
                            'content_host2': "youtube.com",
                            'content_host3': "youtu.be",
                            'content_host4': "vine.co",
                            'activity1': 'load',
                            'ev_date1': params['from_date'],
                            'ev_date2': params['to_date']},
                    index_col = ['ev_date', 'content_host'])

    events_bycontent_play_df = pd.read_sql('''select ev_date, content_host, sum(act_count) as played
                           from events
                           where client_host = %(client_host)s
                             and ( content_host = %(content_host1)s or
                                   content_host = %(content_host2)s or
                                   content_host = %(content_host3)s or
                                   content_host = %(content_host4)s )
                            and activity = %(activity1)s
                            and ( ev_date between %(ev_date1)s and %(ev_date2)s )
                           group by ev_date, content_host
                           order by ev_date, content_host
                    ''', \
                     db_engine, \
                     params={'client_host': params['client'],
                            'content_host1': "instagram.com",
                            'content_host2': "youtube.com",
                            'content_host3': "youtu.be",
                            'content_host4': "vine.co",
                            'activity1': 'play',
                            'ev_date1': params['from_date'],
                            'ev_date2': params['to_date']
                    },
                     index_col = ['ev_date', 'content_host'])
    events_by_content_df = events_bycontent_load_df.join(events_bycontent_play_df)
    events_by_content_df['ratio'] = ((events_by_content_df['played'] / events_by_content_df['loaded']) * 100).round(1)
    events_flat_df = events_by_content_df.stack(0).unstack(1).unstack(1)
    return events_flat_df.fillna(0)


def get_events_by_content(db_engine, params):
    content_load_df = pd.read_sql('''select content_url, sum(act_count) as loaded
                           from events
                           where client_host = %(client_host)s
                            and activity = %(activity1)s
                            and ( ev_date between %(ev_date1)s and %(ev_date2)s )
                           group by content_url, content_host
                           having sum(act_count) > 0
                           order by sum(act_count) desc
                    ''', \
                     db_engine, \
                     params={'client_host': params['client'],
                            'content_host1': "instagram.com",
                            'content_host2': "youtube.com",
                            'content_host3': "youtu.be",
                            'content_host4': "vine.co",
                            'activity1': 'load',
                            'ev_date1': params['from_date'],
                            'ev_date2': params['to_date']
                    },
                     index_col=['content_url'])

    content_play_df = pd.read_sql('''select content_url, sum(act_count) as played
                           from events
                           where client_host = %(client_host)s
                            and activity = %(activity1)s
                            and ( ev_date between %(ev_date1)s and %(ev_date2)s )
                           group by content_url, content_host
                           having sum(act_count) > 0
                    ''', \
                     db_engine, \
                     params={'client_host': params['client'],
                            'content_host1': "instagram.com",
                            'content_host2': "youtube.com",
                            'content_host3': "youtu.be",
                            'content_host4': "vine.co",
                            'activity1': 'play',
                            'ev_date1': params['from_date'],
                            'ev_date2': params['to_date']
                    },
                     index_col ='content_url')
    content_df = content_load_df.join(content_play_df).fillna(0)
    return content_df
