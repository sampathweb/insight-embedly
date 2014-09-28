from urlparse import urlparse
import json
import httpagentparser
from mrjob.job import MRJob
from mrjob.protocol import ReprValueProtocol


def ustr(val):
    try:
        uval = str(val)
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

    OUTPUT_PROTOCOL = ReprValueProtocol

    def mapper(self, _, line):
        row = json.loads(line)
        row_key = {}
        if row['query'].get('c') != 'video':
            return
        row_key['client_key'] = ustr(row['clientKey'])
        row_key['uid'] = ustr(row['query'].get('uid', ''))
        row_key['timestamp'] = row['timestamp']
        row_key['access_class'] = ustr(row['access_class'])
        row_key['endpoint'] = ustr(row['endpoint'])
        row_key['action'] = row['query'].get('a', '')
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
        row_key['status_code'] = row['statusCode']

        yield row_key, 10  # row_in['query'].get('l')

    def reducer(self, row_key, values):
        delim = '\t'
        row_str = ''
        row_str += row_key['client_key'] + delim
        row_str += row_key['uid'] + delim
        row_str += row_key['access_class'] + delim
        row_str += row_key['endpoint'] + delim
        row_str += row_key['action'] + delim
        row_str += row_key['content_type'] + delim
        row_str += row_key['client_host'] + delim
        row_str += row_key['client_url'] + delim
        row_str += row_key['content_host'] + delim
        row_str += row_key['content_url'] + delim
        row_str += str(row_key['timestamp']) + delim
        row_str += row_key.get('client_ip', '') + delim
        row_str += str(1) + delim  # Event Begin
        row_str += str(10) + delim  # Event End
        row_str += str(row_key['status_code'])

        yield None, row_str


if __name__ == '__main__':
    ProcessEventLog.run()
