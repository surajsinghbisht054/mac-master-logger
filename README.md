# Mac-Master-logger

## Installation

```
pip install git+https://github.com/surajsinghbisht054/mac-master-logger
```

## Sample Config

```
from maclogger.maclogger import Maclogger

mac = Maclogger("__YOUR__UUID", '__ENDPOINT__')

logger = mac.create_logger("__LOGGER_NAME__")

logger.error("..")
logger.info("..")
logger.debug("..")

```