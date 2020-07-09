from typing import Dict
from unittest.mock import Mock

from behave import given, then, when

from cloudalerts.v1.alerts import AlertUtils
from cloudalerts.v1.loggers.alert_logging import AlertLogger
from cloudalerts.v1.loggers.cloud_logging import CloudLogging
from tests.bdd.steps.parent_step import ParentStep


class AlertSteps(ParentStep):
    response: Dict = None

    @given("error code folder {path}")
    def error_code(self, path):
        AlertUtils.initialize(path)

    @when("we alert")
    def we_alert(self):
        error_code = None
        param_dict = dict()
        for row in self.table:
            key = row["key"]
            value = row["value"]
            param_dict.update({key: value})
            if key == "ERROR_CODE":
                error_code = value

        self.response = AlertUtils.get_alerting_info_parameterize(
            error_code, param_dict
        )

    @when("we alert {error_code}")
    def we_alert_error(self, error_code):
        # integrations.error_codes = alerts_test_folder
        self.response = AlertUtils.get_alerting_info(error_code)

    @then("template is set with")
    def setup_template(self):
        for row in self.table:
            key = row["key"]
            value = row["value"]
            assert self.response[key] == value

    @given("the client logger is {cloud_client}")
    def step_impl(self, cloud_client):
        CloudLogging.alert_logger = AlertLogger(client=Mock())
