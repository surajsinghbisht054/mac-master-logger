# Mac-Master-logger

## Installation

```
pip install git+https://github.com/surajsinghbisht054/mac-master-logger
```

## Sample Config

```
[machine_details]
uuid = YOUR_UUID
host = HOST_ID

[log_file_paths]
file1 = file_path
file2 = file_path
..
..

```

## Crontab 
```
*/5 * * * * python3 /home/ubuntu/mac-master-logger/main.py >> /home/ubuntu/cron>

```