import logging
import requests_async as requests
import json
import datetime as dt
import asyncio

__version__ = 'dev'

class RequestsHandler(logging.Handler):
    
        def __init__(self, uuid, host):
            logging.Handler.__init__(self)
            self.uuid = uuid
            self.host = host
            
        def emit(self, record):
            log_entry = self.format(record)
            print(log_entry)
            req = requests.post(self.host,
                                json=log_entry, headers={"Content-type": "application/json", "uuid": self.uuid})

            asyncio.run(req)
            
class FormatterLogger(logging.Formatter):
    converter=dt.datetime.fromtimestamp

    def __init__(self, task_name=None):
        super(FormatterLogger, self).__init__()

    def format(self, record):
        ct = self.converter(record.created)
        t = ct.strftime("%Y-%m-%d %H:%M:%S.%f")
        
        data = {'message': record.msg,
                'funcName': record.funcName,
                'lineno': record.lineno,
                'levelname': record.levelname,
                'timestamp': t,
                }

        return json.dumps(data)


class Maclogger:
    def __init__(self, uuid, host):
        self.uuid = uuid
        self.host = host
    
    def create_logger(self, name):
        logger = logging.getLogger(name)
        custom_handler = RequestsHandler(self.uuid, self.host)
        formatter = FormatterLogger(logger)
        custom_handler.setFormatter(formatter)
        logger.addHandler(custom_handler)
        logger.setLevel(logging.DEBUG)
        return logger
    

