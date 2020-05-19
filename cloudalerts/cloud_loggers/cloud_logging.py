import logging

import google.cloud.logging

from cloudalerts.alerts.alerter import Alerter


class CloudLogging:
    class __CloudLogger:
        def __init__(self, client):
            self.logger = logging.getLogger(__name__)

            if self.logger.hasHandlers():
                self.logger.handlers.clear()

            self.logger.addHandler(logging.StreamHandler())
            self.g_logger = client.logger(__name__)
            self.alerter = Alerter().get_instance()

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
            self.log_struct(self.alerter.get_alerting_info(error_code=error_code))

    __instance = None

    def __init__(self, client=google.cloud.logging.Client()):
        if CloudLogging.__instance is None:
            CloudLogging.__instance = CloudLogging.__CloudLogger(client=client)

    def get_logger(self):
        return self.__instance

    def get_instance(self):
        return self.__instance
