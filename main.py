import requests_async as requests
import asyncio
from pygtail import Pygtail
import configparser
import argparse
import os
# ---------------------------------------------------------
# ----------------- CONFIG FILE READ ----------------------
# ---------------------------------------------------------

path_to_config = os.path.join(os.getcwd(), 'config.ini')
config_obj = configparser.ConfigParser()
config_obj.read(path_to_config)

machine_details = config_obj["machine_details"]

host = machine_details["host"]
uuid = machine_details['uuid']

log_paths = list()

path_items = config_obj.items("log_file_paths")
for key, path in path_items:
    log_paths.append(path)
    


def send_request(log_data):
    data = {
        "format" : "simple",
        "log_list" : log_data
    }
    req = requests.post(host, json=data, headers={"Content-type": "application/json", "uuid": uuid})
    asyncio.run(req)


def run_read_log():
    log_list  = list()
    for i in log_paths:
        tail = Pygtail(i, read_from_end=True)
        for log in tail:
            log_list.append(log)
    
    if log_list:
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
        

