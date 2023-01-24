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
*/5 * * * * PATH_TO_YOUR_PYTHON PATH_TO_MAINFILE >> LOGFILE_PATH 2>&1
```



