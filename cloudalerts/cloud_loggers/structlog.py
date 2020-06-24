# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from google.cloud.logging import Client
from google.cloud.logging import _helpers
from google.cloud.logging.handlers import CloudLoggingHandler
from google.cloud.logging.handlers.transports.background_thread import _Worker

from pythonjsonlogger import jsonlogger

import structlog

import datetime
import json
import logging

from structlog import threadlocal, stdlib, processors

from cloudalerts.cloud_loggers.log_filter import censor_header


def monkeypatch_google_enqueue():
    def decode_json_then_enqueue(
        self, record, message, resource=None, labels=None, trace=None, span_id=None
    ):
        try:
            info = json.loads(message)
        except json.decoder.JSONDecodeError:
            info = {"message": message}
        finally:
            info["python_logger"] = record.name
        queue_entry = {
            "info": info,
            "severity": _helpers._normalize_severity(record.levelno),
            "resource": resource,
            "labels": labels,
            "trace": trace,
            "span_id": span_id,
            "timestamp": datetime.datetime.utcfromtimestamp(record.created),
        }
        self._queue.put_nowait(queue_entry)

    _Worker.enqueue = decode_json_then_enqueue


def event_uppercase(logger, method_name, event_dict):
    event_dict["event"] = event_dict["event"].upper()
    return event_dict


def configure_structlog():
    structlog.configure(
        context_class=threadlocal.wrap_dict(dict),
        logger_factory=stdlib.LoggerFactory(),
        wrapper_class=stdlib.BoundLogger,
        processors=[
            # Filter only the required log levels into the log output
            stdlib.filter_by_level,
            # Adds logger=module_name (e.g __main__)
            stdlib.add_logger_name,
            # Uppercase structlog's event name which shouldn't be convoluted with AWS events.
            event_uppercase,
            # Censor secure data
            censor_header,
            # Allow for string interpolation
            stdlib.PositionalArgumentsFormatter(),
            # Render timestamps to ISO 8601
            processors.TimeStamper(fmt="iso"),
            # Include the stack dump when stack_info=True
            processors.StackInfoRenderer(),
            # Include the application exception when exc_info=True
            # e.g log.exception() or log.warning(exc_info=True)'s behavior
            processors.format_exc_info,
            # Decodes the unicode values in any kv pairs
            processors.UnicodeDecoder(),
            # Creates the necessary args, kwargs for log()
            stdlib.render_to_log_kwargs,
        ],
        cache_logger_on_first_use=True,
    )


def get_handler(logName):
    handler = CloudLoggingHandler(Client(), logName)
    handler.setFormatter(jsonlogger.JsonFormatter())
    return handler


def setup(log_name=None):
    configure_structlog()
    monkeypatch_google_enqueue()
    if log_name is None:
        try:
            import __main__

            log_name = __main__.__loader__.name.split(".")[0]
        except:
            pass
    handler = get_handler(log_name)
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
