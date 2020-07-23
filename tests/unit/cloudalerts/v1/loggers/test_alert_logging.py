# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import logging
from unittest import mock

import pytest


def test_alert_logging(monkeypatch):
    from cloudalerts.v1.loggers import AlertLogger
    from cloudalerts.v1.alerts.alert_utils import AlertUtils

    class MockLogger:
        def __init__(*args, **kwargs):
            pass

        def logger(*args, **kwargs):
            return mock.MagicMock()

    def mock_gai(*args, **kwargs):
        return {}

    monkeypatch.setattr(AlertUtils, "get_alerting_info", mock_gai)

    a_logger = AlertLogger(MockLogger())
    a_logger.log_struct_message("This is a message")
    a_logger.log_alert_message("This is also a message")
    a_logger.log_alert_by_error_code("E110001")
