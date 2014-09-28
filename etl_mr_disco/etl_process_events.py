import os
import json
import glob
from collections import OrderedDict, defaultdict
import cStringIO
from boto.s3.connection import S3Connection
from boto.s3.key import Key


def dict_to_string(row, delim='\t'):
    row_str = ''
    for val in row.values():
        try:
            uval = str(val)
        except UnicodeEncodeError:
            uval = val.encode('ascii', 'ignore')
        row_str += '\t' + uval if row_str else uval
    return row_str

if __name__ == '__main__':
    path_in = '../data_raw'
    path_out = '../data_out'
    s3_bucket_name = 'insight-ramesh'
    folder_out = 'embedly-events'
    s3_conn = S3Connection()
    s3_bucket = s3_conn.get_bucket(s3_bucket_name)  # validate=False
    file_pattern = 'events:time:1410274800-1410276599.json'  # 'events:time:*.json'
    for filename_in in glob.glob(os.path.join(path_in, file_pattern)):
        data_out = defaultdict(cStringIO.StringIO)
        with open(filename_in, 'r') as f_in:
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
                    row_out['q_ev_beg'] = None
                    row_out['q_ev_end'] = None

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
                            row_out['q_ev_beg'] = None
                            row_out['q_ev_end'] = None
                            process_range = process_time.split('-')
                            if process_range:
                                if process_range[0].isdigit():
                                    row_out['q_ev_beg'] = int(process_range[0])
                                if len(process_range) > 1 and process_range[1].isdigit():
                                    row_out['q_ev_end'] = int(process_range[1])
                            data_out['all_files'].write(dict_to_string(row_out, '\t') + "\n")
                    else:
                        # Play or other events
                        row_out['q_ev_beg'] = None
                        row_out['q_ev_end'] = None
                        data_out['all_files'].write(dict_to_string(row_out, '\t') + "\n")
        for client_id, f_out in data_out.iteritems():
            k = Key(s3_bucket)
            k.key = 'embedly_events/' + filename_in.split('/')[-1]
            k.set_contents_from_string(f_out.getvalue())
            f_out.close()
