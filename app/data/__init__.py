import pandas as pd


def get_data_df(filename='simulated_data.csv'):
    df = pd.read_csv(filename, parse_dates=True)
    df.ev_date = pd.to_datetime(df.ev_date)
    return df


def get_video_df(data_df):
    # video_grouped_dt = data_df.groupby(['ev_date', 'video_url']).agg(['median', 'count'])
    video_grouped = data_df.groupby(['video_url']).agg(['median', 'count'])

    video_grouped.to_csv('video_grouped.csv')
    video_df = pd.read_csv('video_grouped.csv', skiprows=3)

    video_df.columns = ['video_url', 'length', 'views']
    video_df = video_df.set_index('video_url')
    return video_df

data_df = get_data_df()
video_df = get_video_df(data_df)
