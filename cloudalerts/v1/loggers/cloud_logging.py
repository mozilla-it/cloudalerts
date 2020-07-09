# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import google.cloud

from cloudalerts.v1.loggers.alert_logging import AlertLogger


class CloudLogging:
    alert_logger: AlertLogger = None

    @classmethod
    def get_logger(cls):
        if cls.alert_logger is None:
            client = google.cloud.logging.Client()
            cls.alert_logger = AlertLogger(client=client)
        return cls.alert_logger
