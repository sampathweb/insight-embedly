import random
import pandas as pd

client = ['reddit.com', 'storify.com', 'guardian.com', 'espn.com']
video_url = ['v_' + str(i) for i in range(20)]
video_source = ['youtube', 'vine', 'vimeo']
uid = ['u_' + str(i) for i in range(100)]
length = range(10, 300)
ev_date = ['09/20/2014', '09/21/2014', '09/22/2014', '09/23/2014', '09/24/2014', '09/25/2014', '09/26/2014']

if __name__ == '__main__':
    data = []
    for line in range(30000):
        row = {}
        row['client'] = random.choice(client)
        row['video_url'] = random.choice(video_url)
        row['video_source'] = random.choice(video_source)
        row['uid'] = random.choice(uid)
        row['length'] = random.choice(length)
        row['ev_date'] = random.choice(ev_date)

        data.append(row)

    df = pd.DataFrame(data)
    df.to_csv('simulated_data.csv', index=False)
