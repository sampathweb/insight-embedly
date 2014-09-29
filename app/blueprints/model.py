import pandas as pd


def get_events_date_df(db_engine):
    events_bydate_df = pd.read_sql('''select ev_date, activity, sum(act_count) as act_count
                             from events
                             where client_host = %(client_host)s
                               and ( content_host = %(content_host1)s or
                                     content_host = %(content_host2)s or
                                     content_host = %(content_host3)s or
                                     content_host = %(content_host4)s or
                                     content_host = %(content_host5)s )
                              and ( activity = %(activity1)s or
                                    activity = %(activity2)s )
                             group by ev_date, activity
                             having sum(act_count) > 100
                             order by ev_date, activity

                            ''', \
                        db_engine, \
                        params={'client_host': "storify.com",
                              'content_host1': "instagram.com",
                              'content_host2': "youtube.com",
                              'content_host3': "youtu.be",
                              'content_host4': "soundcloud.com",
                              'content_host5': "vine.co",
                              'activity1': 'load',
                              'activity2': 'play',
                              'ev_date1': '2014-09-20',
                              'ev_date2': '2014-09-24'},
                        index_col = ['ev_date', 'activity'])
    return events_bydate_df


def get_events_by_source_df(db_engine):
    events_bycontent_load_df = pd.read_sql('''select content_host, sum(act_count) as loaded
                           from events
                           where client_host = %(client_host)s
                             and ( content_host = %(content_host1)s or
                                   content_host = %(content_host2)s or
                                   content_host = %(content_host3)s or
                                   content_host = %(content_host4)s or
                                   content_host = %(content_host5)s )
                            and activity = %(activity1)s
                            and ( ev_date between %(ev_date1)s and %(ev_date2)s )
                           group by content_host
                           order by content_host
                    ''', \
                     db_engine, \
                     params={'client_host': "storify.com",
                            'content_host1': "instagram.com",
                            'content_host2': "youtube.com",
                            'content_host3': "youtu.be",
                            'content_host4': "soundcloud.com",
                            'content_host5': "vine.co",
                            'activity1': 'load',
                            'ev_date1': '2014-09-20',
                            'ev_date2': '2014-09-24'
                    },
                     index_col = ['content_host'])

    events_bycontent_play_df = pd.read_sql('''select content_host, sum(act_count) as played
                           from events
                           where client_host = %(client_host)s
                             and ( content_host = %(content_host1)s or
                                   content_host = %(content_host2)s or
                                   content_host = %(content_host3)s or
                                   content_host = %(content_host4)s or
                                   content_host = %(content_host5)s )
                            and activity = %(activity1)s
                            and ( ev_date between %(ev_date1)s and %(ev_date2)s )
                           group by content_host
                           order by content_host
                    ''', \
                     db_engine, \
                     params={'client_host': "storify.com",
                            'content_host1': "instagram.com",
                            'content_host2': "youtube.com",
                            'content_host3': "youtu.be",
                            'content_host4': "soundcloud.com",
                            'content_host5': "vine.co",
                            'activity1': 'play',
                            'ev_date1': '2014-09-20',
                            'ev_date2': '2014-09-24'
                    },
                     index_col = ['content_host'])
    events_by_content_df = events_bycontent_load_df.join(events_bycontent_play_df)
    return events_by_content_df
