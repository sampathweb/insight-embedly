import os
import sys
import math
import json
import glob
from urlparse import urlparse
from collections import OrderedDict, defaultdict
import cStringIO
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from boto.s3 import connect_to_region
from filechunkio import FileChunkIO
import httpagentparser


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

def dict_to_string(row, delim='\t'):
    row_str = ''
    row_str += ustr(row['client_key']) + delim
    row_str += ustr(row['q_uid']) + delim
    row_str += ustr(row['access_class']) + delim
    row_str += ustr(row['endpoint']) + delim
    row_str += ustr(row['endpoint_ver']) + delim
    row_str += ustr(row['q_a']) + delim
    row_str += ustr(row['q_c']) + delim
    # row_str += ustr(row['q_s']) + delim
    url_embeded = ustr(row['q_u'][:100])
    url_embed = ustr(row['q_r'][:100])
    row_str += get_url_host(url_embeded) + delim
    row_str += url_embeded + delim
    row_str += get_url_host(url_embed) + delim
    row_str += url_embed + delim
    row_str += ustr(row['timestamp']) + delim
    row_str += ustr(row['client_ip']) + delim
    row_str += ustr(row['q_ev_beg']) + delim
    row_str += ustr(row['q_ev_end']) + delim
    user_agent = ustr(row['h_user_agent'])
    try:
        parsed_ua = httpagentparser.detect(user_agent)
        user_os = parsed_ua['os'].get('name', '')
        user_browser = parsed_ua['browser'].get('name', '')
    except:
        user_os = ''
        user_browser = ''
    row_str += user_os + delim
    row_str += user_browser + delim
    row_str += ustr(row['status_code'])
    return row_str


def send_file_boto(file_path, bucket):
    # Get file info
    source_size = os.stat(file_path).st_size
    mp = bucket.initiate_multipart_upload(os.path.basename(file_path))
    # Use a chunk size of 50 MiB (feel free to change this)
    chunk_size = 52428800
    chunk_count = int(math.ceil(source_size / chunk_size))
    for i in range(chunk_count + 1):
        offset = chunk_size * i
        bytes = min(chunk_size, source_size - offset)
        with FileChunkIO(file_path, 'r', offset=offset,
                         bytes=bytes) as fp:
            mp.upload_part_from_file(fp, part_num=i + 1)
    # Finish the upload
    mp.complete_upload()

if __name__ == '__main__':
    path_in = '../data_raw'
    path_out = '../data_out'
    s3_bucket_name = 'insight-ramesh'
    folder_out = 'embedly_events'
    # connect_to_region('us_west_2')
    s3_conn = S3Connection()
    s3_bucket = s3_conn.get_bucket(s3_bucket_name)  # validate=False
    file_pattern = 'events:time:*.json'  # 'events:time:*.json'
    for filename_in in glob.glob(os.path.join(path_in, file_pattern)):
        data_out = defaultdict(cStringIO.StringIO)
        filename_out = os.path.join(path_out, filename_in.split('/')[-1])
        with open(filename_in, 'r') as f_in, open(filename_out, 'w') as f_out:
            for line in f_in:
                row_in = json.loads(line)
                if row_in['query'].get('c') == 'video':  # data_in['clientKey'] and data_in['timestamp']:
                    row_out = OrderedDict()
                    row_out['access_class'] = row_in['access_class']
                    row_out['endpoint'] = row_in['endpoint']
                    row_out['timestamp'] = row_in['timestamp']
                    row_out['user_eid'] = row_in.get('user-eid', '')

                    # row_out['h_referrer'] = row_in['headers'].get('referrer', '')
                    row_out['h_user_agent'] = row_in['headers'].get('user-agent', '')

                    row_out['endpoint_ver'] = row_in.get('user-endpointVersion', 0)
                    row_out['eid_generated'] = row_in.get('eid_generated', '')

                    row_out['q_a'] = row_in['query'].get('a', '')
                    row_out['q_c'] = row_in['query'].get('c', '')
                    row_out['q_uid'] = row_in['query'].get('uid', '')
                    row_out['q_g'] = row_in['query'].get('g', '')
                    row_out['q_s'] = row_in['query'].get('s', '')
                    row_out['q_r'] = row_in['query'].get('r', '')
                    row_out['q_u'] = row_in['query'].get('u', '')
                    row_out['q_t'] = row_in['query'].get('t', '')
                    row_out['q_key'] = row_in['query'].get('key', '')
                    row_out['q_sid'] = row_in['query'].get('sid', '')
                    row_out['q_ev_beg'] = 0
                    row_out['q_ev_end'] = 0

                    row_out['client_ip'] = row_in.get('clientIp', '')
                    row_out['client_key'] = row_in['clientKey']
                    row_out['status_code'] = row_in['statusCode']

                    process_field = row_in['query'].get('l')
                    if process_field:
                        # Progress Event
                        if isinstance(process_field, list):
                            process_times = process_field
                        else:
                            process_times = process_field.split(',')
                        for process_time in process_times:
                            row_out['q_ev_beg'] = 0
                            row_out['q_ev_end'] = 0
                            process_range = process_time.split('-')
                            if process_range:
                                if process_range[0].isdigit():
                                    row_out['q_ev_beg'] = int(process_range[0])
                                if len(process_range) > 1 and process_range[1].isdigit():
                                    row_out['q_ev_end'] = int(process_range[1])
                            f_out.write(dict_to_string(row_out, '\t') + "\n")
                    else:
                        # Play or other events
                        row_out['q_ev_beg'] = 0
                        row_out['q_ev_end'] = 0
                        f_out.write(dict_to_string(row_out, '\t') + "\n")
        # send_file_boto(filename_out, s3_bucket)
