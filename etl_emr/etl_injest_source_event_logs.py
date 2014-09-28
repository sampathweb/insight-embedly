from urlparse import urlparse
import json
import datetime
import pytz
import httpagentparser
from collections import defaultdict
from mrjob.job import MRJob
from mrjob.protocol import RawValueProtocol


def ustr(val):
    try:
        uval = str(val) if val else ''
    except UnicodeEncodeError:
        uval = val.encode('ascii', 'ignore')
    return uval


def get_url_host(url_path):
    try:
        url_host = urlparse(url_path).netloc
        if url_host.startswith('www.'):
            url_host = url_host[4:]
    except:
        url_host = ''
    return url_host


class ProcessEventLog(MRJob):

    OUTPUT_PROTOCOL = RawValueProtocol  # ReprValueProtocol

    # def mapper_pre_filter(self):
    #     return 'grep "c": "video"'

    def extract_act_length(self, act_value):
        act_len = 0
        if act_value:
            # Progress Event
            if isinstance(act_value, list):
                act_intervals = act_value
            else:
                act_intervals = act_value.split(',')
            for act_interval in act_intervals:
                act_range = act_interval.split('-')
                if act_range:
                    if act_range[0].isdigit():
                        beg_val = int(act_range[0])
                        if len(act_range) > 1 and act_range[1].isdigit():
                            end_val = int(act_range[1])
                            if end_val > beg_val:
                                act_len += end_val - beg_val
        return act_len

    def mapper(self, _, line):
        error = False
        row_key = {}
        row_val = {}
        try:
            row = json.loads(line)
        except ValueError:
            error = True
        if not error and row['query'].get('c') == 'video':
            row_key['client_key'] = ustr(row.get('clientKey', ''))
            row_key['client_ip'] = ustr(row.get('clientIp', ''))
            row_key['uid'] = ustr(row['query'].get('uid', ''))
            if not row_key['uid']:
                row_key['uid'] = row_key['client_ip']
            row_key['sid'] = ustr(row['query'].get('sid', ''))
            row_timestamp = row['timestamp']
            try:
                row_key['ev_date'] = datetime.datetime.fromtimestamp(row_timestamp, pytz.utc).strftime('%Y-%m-%d')
            except:
                error = True
            row_key['content_type'] = row['query'].get('c', '')
            url_embed = ustr(row['query'].get('r', '')[:100])
            row_key['client_host'] = get_url_host(url_embed)
            row_key['client_url'] = url_embed
            url_embeded = ustr(row['query'].get('u', '')[:100])
            row_key['content_host'] = get_url_host(url_embeded)
            row_key['content_url'] = url_embeded
            user_agent = ustr(row['headers'].get('user-agent', ''))
            try:
                parsed_ua = httpagentparser.detect(user_agent)
                row_key['os'] = parsed_ua['os'].get('name', '')
                row_key['browser'] = parsed_ua['browser'].get('name', '')
            except:
                row_key['os'] = ''
                row_key['browser'] = ''
            row_val['timestamp'] = row_timestamp
            row_val['activity'] = row['query'].get('a', '')
            row_val['act_count'] = 1  # row['query'].get('l', '')
            row_val['act_length'] = self.extract_act_length(row['query'].get('l', ''))
        if not error:
            yield row_key, row_val

    def act_default_val(self):
        return {'act_count': 0, 'act_length': 0}

    def reducer(self, row_key, values):
        delim = '\t'
        if row_key:
            row_kstr = ''
            row_kstr += row_key['ev_date'] + delim
            row_kstr += row_key.get('client_key', '') + delim
            row_kstr += row_key.get('client_ip', '') + delim
            row_kstr += row_key.get('uid', '') + delim
            row_kstr += row_key.get('sid', '') + delim
            row_kstr += row_key['content_type'] + delim
            row_kstr += row_key['client_host'] + delim
            row_kstr += row_key['client_url'] + delim
            row_kstr += row_key['content_host'] + delim
            row_kstr += row_key['content_url'] + delim
            row_kstr += row_key['os'] + delim
            row_kstr += row_key['browser'] + delim
            #  Parse the Events

            events = defaultdict(self.act_default_val)
            for row_val in values:
                act = row_val.get('activity', '')
                events[act]['act_count'] += row_val.get('act_count', 0)
                events[act]['act_length'] += row_val.get('act_length', 0)

            for act_key, act_val in events.iteritems():
                row_out = row_kstr
                row_out += str(1) + delim  # Row Count
                row_out += act_key + delim
                row_out += str(act_val['act_count']) + delim
                row_out += str(act_val['act_length'])
                yield None, row_out


if __name__ == '__main__':
    ProcessEventLog.run()
