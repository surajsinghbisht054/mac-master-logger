import requests
from pygtail import Pygtail
import configparser
import argparse
import os
import re
import datetime as dt
# ---------------------------------------------------------
# ----------------- CONFIG FILE READ ----------------------
# ---------------------------------------------------------

today = dt.date.today()
DEFAULT_YEAR = str(today.year)

base_path = os.path.dirname(os.path.realpath(__file__))

config_obj = configparser.ConfigParser()
config_obj.read(os.path.join(base_path, 'config.ini'))

machine_details = config_obj["machine_details"]

host = machine_details["host"]
uuid = machine_details['uuid']

log_paths = list()

path_items = config_obj.items("log_file_paths")
for key, path in path_items:
    log_paths.append([key, path])

patterns = {
    "syslog": r"((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\ \d+\ \d+\:\d+:\d+) ip-\d+-\d+-\d+-\d+\ ([a-zA-Z]+)(.+)",
    "timestamp" : r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{3}'
}

def getting_date_python(date_string):
    date_patterns = ['%Y-%m-%d %H:%M:%S.%f','%Y-%m-%d %H:%M:%S,%f', '%Y-%m-%d %H:%M:%S', '%b %d %H:%M:%S%Y']
    
    for i in date_patterns:
        try:
            return dt.datetime.strptime(date_string, i)
        except ValueError:
            pass

def send_request(log_data):
    data = {
        "format" : "simple",
        "log_list" : log_data
    }
    requests.post(host, json=data, headers={"Content-type": "application/json", "uuid": uuid})


def run_read_log():
    log_list  = list()
    for i in log_paths:
        tail = Pygtail(i[1], read_from_end=True)
        for log in tail:
            # Check log type
            log_type = i[0].lower()
            log_data = dict()
            if log_type == 'syslog':
                result = re.search(patterns[log_type], log)
                if result:
                    timestamp = result.group(1) + DEFAULT_YEAR
                    timestamp = getting_date_python(timestamp)
                    timestamp+= dt.timedelta(hours=5,minutes=30)
                    log_data = {
                        'log_type': i[0],
                        'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S.%f'),
                        'service': result.group(2),
                        'message': result.group(3)
                    } 
            else:
                result = re.findall(patterns['timestamp'], log)
                if result:
                    timestamp = getting_date_python(result[0])
                    log_data = {
                        'log_type': i[0],
                        'timestamp': timestamp.strftime("%Y-%m-%d %H:%M:%S.%f"),
                        'service': i[0],
                        'message': log
                    }
            log_list.append(log_data)
   
    if log_list:
        print("Sending Log List")
        send_request(log_list)
    else:
        print("List is Empty!")

def run_initial_read_log():
    for i in log_paths:
        tail = Pygtail(i, read_from_end=True)
        for log in tail:
            print(log)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-test", "--testing", action="store_true")
    args = parser.parse_args()

    if args.testing:
        run_initial_read_log()
    else:
        run_read_log()