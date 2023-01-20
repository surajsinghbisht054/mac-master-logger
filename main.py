import requests_async as requests
import asyncio
from pygtail import Pygtail
import configparser

config_obj = configparser.ConfigParser()
config_obj.read("config.ini")

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
        for log in Pygtail(i):
            log_list.append(log)

    send_request(log_list)

