# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import logging
import sys

from deprecated import deprecated

from cloudalerts.v1.alerts import AlertUtils

__excepthook__ = None


class AlertLogger:
    def __init__(self, client, install_sys_hook=True):
        if install_sys_hook:
            self.install_sys_hook()
        self.logger = logging.getLogger(__name__)

        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        self.logger.addHandler(logging.StreamHandler())
        self.g_logger = client.logger(__name__)

    def install_sys_hook(self):
        global __excepthook__

        if __excepthook__ is None:
            __excepthook__ = sys.excepthook

        def handle_exception(*exc_info):
            self.error(f"FATAL EXCEPTION->{exc_info}")
            __excepthook__(*exc_info)

        sys.excepthook = handle_exception

    def info(self, msg: str, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg: str, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def debug(self, msg: str, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def error(self, msg: str, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    def log_alert_info(self, info, client=None, **kw):
        self.g_logger.log_struct(info)

    @deprecated(reason="You should use another function")
    def log_struct(self, info, client=None, **kw):
        self.g_logger.log_struct(info)

    @deprecated(reason="You should use another function")
    def log_struct_message(self, message: str):
        dictionary = dict()
        dictionary["MESSAGE"] = message
        self.log_struct(dictionary)

    def log_alert_message(self, message: str):
        dictionary = dict()
        dictionary["MESSAGE"] = message
        self.log_struct(dictionary)

    def log_alert_by_error_code(self, error_code: str):
        self.log_struct(AlertUtils.get_alerting_info(error_code=error_code))
