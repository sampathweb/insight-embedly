from collections import namedtuple
from numpy import median
from mrjob.job import MRJob
from mrjob.protocol import ReprValueProtocol


class AggregateByContent(MRJob):

    OUTPUT_PROTOCOL = ReprValueProtocol

    EventRow = namedtuple('EventRow', ['ev_date', 'client_key', 'client_ip', \
        'uid', 'sid', 'content_type', 'client_host', 'client_url', \
        'content_host', 'content_url', 'os', 'browser', \
        'row_count', 'activity', 'act_count', 'act_length'])

    def mapper(self, _, line):
        row = line.split('\\t')
        event_row = self.EventRow._make(row)
        row_key = {}
        row_key['ev_date'] = event_row.ev_date
        row_key['client_host'] = event_row.client_host
        row_key['content_host'] = event_row.content_host
        row_key['content_url'] = event_row.content_url
        row_val = {}
        row_val['activity'] = event_row.activity
        row_val['act_count'] = event_row.act_count
        row_val['act_length'] = event_row.act_length
        row_val['row_count'] = event_row.row_count
        import ipdb;ipdb.set_trace()
        yield row_key, row_val

    def reducer(self, row_key, values):
        delim = '\t'
        if row_key:
            row_str = ''
            row_str += row_key['ev_date'] + delim
            row_str += row_key['client_host'] + delim
            row_str += row_key['content_host'] + delim
            row_str += row_key['content_url'] + delim
            progress_lengths = []
            play_counts = []
            view_counts = []
            for row_val in values:
                if row_val['activity'] == 'progress':
                    progress_lengths.append(row_val['act_length'])
                if row_val['activity'] == 'play':
                    play_counts.append(row_val['row_count'])
                if row_val['activity'] == 'view':
                    view_counts.append(row_val['row_count'])
            row_str += str(median(progress_lengths)) + delim  # Median Play Time
            row_str += str(sum(play_counts)) + delim  # Total Play count
            row_str += str(sum(view_counts))  # Total View count
        yield None, row_str


if __name__ == '__main__':
    AggregateByContent.run()
