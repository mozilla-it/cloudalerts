# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import logging
import socket


# Modelled from:
#   1. https://github.com/mozilla-services/python-dockerflow/blob/master/src/dockerflow/logging.py
#   2. https://wiki.mozilla.org/Firefox/Services/Logging


class SecOpsFormatter(logging.Formatter):
    """Custom stdlib logging formatter for structlog ``event_dict`` messages.
    Apply a structlog processor to the ``event_dict`` passed as
    ``LogRecord.msg`` to convert it to loggable format (a string).
    """

    def __init__(self, processor, fmt=None, datefmt=None, style="%"):
        """"""
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)
        self.processor = processor

    def format(self, record):
        """Extract structlog's ``event_dict`` from ``record.msg``.
        Process a copy of ``record.msg`` since the some processors modify the
        ``event_dict`` and the ``LogRecord`` will be used for multiple
        formatting runs.
        """
        if isinstance(record.msg, dict):
            msg_repr = self.processor(record._logger, record._name, record.msg.copy())
        return msg_repr


def add_type_processor(logger, method_name, event_dict):
    event_dict["Type"] = "request.summary"
    return event_dict


def add_hostname_processor(logger, method_name, event_dict):
    event_dict["Host"] = socket.gethostname()
    return event_dict


def add_pid_processor(logger, method_name, event_dict):
    event_dict["Pid"] = None
    return event_dict


def add_env_version_processor(logger, method_name, event_dict):
    event_dict["EnvVersion"] = ""
    return event_dict


def add_severity_processor(logger, method_name, event_dict):
    if "level" in event_dict:
        event_dict["Severity"] = event_dict["level"]
    return event_dict


def event_dict_to_message(logger, name, event_dict):
    return ((event_dict,), {"extra": {"_logger": logger, "_name": name}})
