# Up and Running

A guide to setting up your application to use the
`CloudLogging` library.  This library provides a mechanism
by which to emit structured application logging to
Google Cloud's Stackdriver service.

## Application Setup

```python
from cloudalerts.cloud_loggers.structlog import setup

setup(log_name="application_logger_name")

# Leveraging structlog to interface with Stackdriver
import structlog
logger = structlog.get_logger()
logger.error("Uhoh, something bad did", moreinfo="it was bad", years_back_luck=5)

# Leveraging the standard logging library to interface with Stackdriver
import logging
logger = logging.getLogger("yoyo")
logger.error("Regular logging calls will work happily too")
```
