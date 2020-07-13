# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Any

import structlog

from cloudalerts.v2.loggers.structlog import setup

LOGGER = None


def get_log(app_name: str = None) -> Any:
    """
    This method either creates and returns or returns an instantiated
    instance of an structured logger that reports to Stackdriver.
    :param app_name:
    :return: a global logger instance
    """
    global LOGGER
    if not LOGGER:
        setup(app_name)
        LOGGER = structlog.get_logger()
    return LOGGER
