# colored-logger
A convenience wrapper around built-in logging instance supporting colors and other small QoL features

## Usage

By default this logger emits messages with color-coded log levels to stderr while simultaneously echoing them to the disk (without color information, of course).

```python
import logging
from colorlogger import get_logger

logger = get_logger(
    scriptname = __file__
)
```

```python
import logging
from colorlogger import get_logger

logger = get_logger(
    scriptname = "myapp",
    log_dir = "/some/dir",  # default: ./logs
    level = logging.WARNING,  # default: DEBUG
    to_stdout = True,  # redirect to stdout (default: stderr)
    persist = False,  # do not echo logs to the disk (default: True)
    pid = True  # attach PID of the current process to log messages (default: False)
)
```
