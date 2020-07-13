# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import json
import logging
import sys
import tempfile

import structlog

from cloudalerts.v2.loggers.secops_formatter import add_env_version_processor
from cloudalerts.v2.loggers.secops_formatter import add_hostname_processor
from cloudalerts.v2.loggers.secops_formatter import add_pid_processor
from cloudalerts.v2.loggers.secops_formatter import add_severity_processor
from cloudalerts.v2.loggers.secops_formatter import add_type_processor
from cloudalerts.v2.loggers.secops_formatter import event_dict_to_message
from cloudalerts.v2.loggers.secops_formatter import SecOpsFormatter


def test_logging():
    # Preamble
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            add_type_processor,
            add_hostname_processor,
            add_pid_processor,
            add_env_version_processor,
            add_severity_processor,
            structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            # Do not include last processor that converts to a string for stdlib
            # since we leave that to the handler's formatter.
            event_dict_to_message,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    handler_stream = logging.StreamHandler(sys.stdout)
    handler_stream.setFormatter(
        SecOpsFormatter(processor=structlog.dev.ConsoleRenderer())
    )
    handler_stream.setLevel(logging.DEBUG)
    tmpfile = tempfile.NamedTemporaryFile(delete=True)
    temp_file_name = tmpfile.name
    handler_file = logging.FileHandler(temp_file_name, encoding="utf-8")
    handler_file.setLevel(logging.INFO)
    handler_file.setFormatter(
        SecOpsFormatter(processor=structlog.processors.JSONRenderer())
    )

    logger = structlog.get_logger("lib")
    logger.setLevel(logging.DEBUG)

    logging.root.setLevel(logging.WARNING)
    logging.root.addHandler(handler_stream)
    logging.root.addHandler(handler_file)

    # Test
    log = structlog.get_logger("lib")

    # Log a few different events.
    log.info("messageA")
    log.info("messageB")
    try:
        raise AssertionError("critical")
    except AssertionError as exc:
        log.exception("some exception", exc=exc)

    # Read the logfile, which contains one JSON string per entry.
    with open(temp_file_name) as log:
        log_json = log.read()
    log = [json.loads(entry) for entry in log_json.splitlines()]
    assert "messageA" in log[0]["event"]
    assert "Host" in log[0]
    assert "Pid" in log[0]
    assert "Type" in log[0]
    assert "Severity" in log[1]
    assert "messageB" in log[1]["event"]
    assert "Host" in log[1]
    assert "Pid" in log[1]
    assert "Severity" in log[1]
    assert "Type" in log[1]
