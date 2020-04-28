import logging

import google.cloud.logging

from cloudalerts.alerts.alert_utils import AlertUtils


class AlertLogger:
    def __init__(self, client):
        self.logger = logging.getLogger(__name__)

        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        self.logger.addHandler(logging.StreamHandler())
        self.g_logger = client.logger(__name__)

    def info(self, msg: str, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg: str, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def debug(self, msg: str, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def error(self, msg: str, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    # deprecated
    def log_struct(self, info, client=None, **kw):
        self.g_logger.log_struct(info, client, **kw)

    def log_alert_info(self, info, client=None, **kw):
        self.g_logger.log_struct(info, client, **kw)

    # deprecated
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


class CloudLogging:
    alert_logger: AlertLogger = None

    @classmethod
    def get_logger(cls):
        if cls.alert_logger is None:
            client = google.cloud.logging.Client()
            cls.logger = AlertLogger(client=client)
        return cls.logger
