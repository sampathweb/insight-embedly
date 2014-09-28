from collections import namedtuple
from numpy import median
from mrjob.job import MRJob
from mrjob.protocol import RawValueProtocol


class AggregateByContent(MRJob):

    OUTPUT_PROTOCOL = RawValueProtocol

    EventRow = namedtuple('EventRow', ['ev_date', 'client_key', 'client_ip', \
        'uid', 'sid', 'content_type', 'client_host', 'client_url', \
        'content_host', 'content_url', 'os', 'browser', \
        'row_count', 'activity', 'act_count', 'act_length'])

    def mapper(self, _, line):
        row = line.split('\t')
        event_row = self.EventRow(*row)
        row_key = {}
        row_key['ev_date'] = event_row.ev_date
        row_key['client_host'] = event_row.client_host
        row_key['content_host'] = event_row.content_host
        row_key['content_url'] = event_row.content_url
        row_val = {}
        row_val['activity'] = event_row.activity
        row_val['act_count'] = int(event_row.act_count)
        row_val['act_length'] = int(event_row.act_length)
        row_val['row_count'] = int(event_row.row_count)
        yield row_key, row_val

    def reducer(self, row_key, values):
        delim = '\t'
        if row_key:
            row_str = ''
            row_str += row_key['ev_date'] + delim
            row_str += row_key['client_host'] + delim
            row_str += row_key['content_host'] + delim
            row_str += row_key['content_url'] + delim
            progress_lengths = [0]
            play_counts = [0]
            view_counts = [0]
            hover_counts = [0]
            for row_val in values:
                if row_val['activity'] == 'progress':
                    progress_lengths.append(row_val['act_length'])
                if row_val['activity'] == 'play':
                    play_counts.append(row_val['row_count'])
                if row_val['activity'] == 'view':
                    view_counts.append(row_val['row_count'])
                if row_val['activity'] == 'hover':
                    hover_counts.append(row_val['row_count'])
            med_prog = median(progress_lengths)
            tot_play = sum(play_counts)
            tot_view = sum(view_counts)
            tot_hover = sum(hover_counts)
            if med_prog > 0 and tot_play == 0:
                tot_play = 1
            if med_prog > 0 and tot_view == 0:
                tot_view = 1
            if med_prog > 0 and tot_hover == 0:
                tot_hover = 1
            row_str += str(tot_view) + delim  # Total View count
            row_str += str(tot_hover) + delim  # Total Hover count
            row_str += str(tot_play) + delim  # Total Play count
            row_str += str(med_prog)  # Median Play Time
        yield None, row_str


if __name__ == '__main__':
    AggregateByContent.run()
