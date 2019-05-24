import pathlib
import os
from tqdm import tqdm
import json
import base64
import re


class Processor():

    def __init__(self, error_string, download_path='download', output_path='output'):
        self.download_path = download_path
        self.output_path = output_path
        self.error_string = error_string

    def run(self):
        print("Collecting bad rows")
        events = []
        for filename in pathlib.Path(self.download_path).glob('**/*.txt'):
            with open(filename) as f:
                lines = [line.rstrip('\n') for line in f]
                for l in lines:
                    events.append((filename, l))
        print("Collected %s events" % len(events))
        parsed_events = []
        for fn, e in tqdm(events, total=len(events)):
            pe = self.parse_event(e, self.error_string)
            if pe is not None:
                parsed_events.append((fn, pe))
        print("Found %s events to output" % len(parsed_events))
        for fn, pe in  tqdm(parsed_events, total=len(parsed_events)):
            fn = str(fn).replace(self.download_path, self.output_path)
            filename = fn.split('/')[-1:][0]
            pathlib.Path(self.output_path).mkdir(parents=True, exist_ok=True)
            with open(self.output_path+'/'+filename, 'w') as f:
                f.write(pe)
        print("Processed!")

    def parse_event(self, event, error_string):
        e = json.loads(event)
        line = e['line']
        errors=e['errors']
        result = None
        for er in errors:
            if error_string in er['message']:
                o = line.split('\t')
                cx = o[16] # payload
                cx = json.loads(self.decode_base64(cx)) #decode
                for i, cx_event in enumerate(cx):
                # CHANGE ME!
                #
                #
                    if 'notification_id' in cx_event:
                        cx_event['notification_id'] = str(cx_event['notification_id'])
                        cx[i] = cx_event
                #
                #
                cx = bytes(json.dumps(cx), 'utf-8')
                cx = base64.standard_b64encode(cx)
                o[16] = cx.decode('utf-8')
                o = '\t'.join(o)
                return o




    def decode_base64(self, s):
        # parts = s.split('-')
        # ret = []
        # for p in parts:
        s += '=' * (-len(s) % 4)
        try:
            # ret.append(base64.urlsafe_b64decode(p).decode('utf-8'))
            return base64.urlsafe_b64decode(s).decode('utf-8')
        except:
            print(s)
            return s
        # return ''.join(ret)
