# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import imp
import json
import os
import tempfile

import cachetools

import cloudalerts.v2.alerts.alert_utils
from cloudalerts.v2.alerts.alert_utils import AlertUtils


def test_get_number_of_errors_when_empty():
    alert_utils = AlertUtils("doesnt_matter")
    assert alert_utils.get_length() == 0


def test_get_number_of_errors_when_non_empty():
    alert_utils = AlertUtils("doesnt_matter")
    alert_utils.add("FAKE", 1)
    assert alert_utils.get_length() == 1
    alert_utils.acknowledge_errors()
    assert alert_utils.get_length() == 0


def test_load_error_details_given_valid_error_content(monkeypatch):
    content = {
        "Error_Code": "{{page.ERROR_CODE}}",
        "Alert_Condition": "System was not able to do expected operation.",
        "Severity": "High",
        "Alert_Message": "Could not perform expected operation. This could result in duplicate entries.",
        "Recipient": "#operation-channel",
        "Suggested_Actions": "Forward Alert to Respective Team",
        "Escalation_Procedure": "operations_support@mozilla.com",
        "Notification_Channel": "{{page.NOTIFICATION_CHANNEL}}",
    }
    tempf = create_temp_file_from_url(file_content=json.dumps(content))
    directory = os.path.dirname(tempf.name)
    file_path = str(tempf.name)
    error_code_as_file_name = os.path.basename(file_path)
    error_code_as_file_name_without_extentions = os.path.splitext(
        error_code_as_file_name
    )[0]
    alert_utils = AlertUtils(directory)
    assert directory == alert_utils.path_to_err_templates
    # alert_utils.errors.update({error_code_as_file_name_without_extentions: alert_utils._AlertUtils__load(error_code=error_code_as_file_name_without_extentions)})
    assert content == alert_utils.get_error_details(
        error_code=error_code_as_file_name_without_extentions
    )
    # again with the "cache"
    alert_utils = AlertUtils(directory)
    assert directory == alert_utils.path_to_err_templates
    alert_utils.errors.update(
        {
            error_code_as_file_name_without_extentions: alert_utils._AlertUtils__load(
                error_code=error_code_as_file_name_without_extentions
            )
        }
    )
    assert content == alert_utils.get_error_details(
        error_code=error_code_as_file_name_without_extentions
    )


def test_render_error_template_given_valid_error_content():
    content = {
        "Error_Code": "{{page.ERROR_CODE}}",
        "Alert_Condition": "System was not able to do expected operation.",
        "Severity": "High",
        "Alert_Message": "Could not perform expected operation. This could result in duplicate entries.",
        "Recipient": "#operation-channel",
        "Suggested_Actions": "Forward Alert to Respective Team",
        "Escalation_Procedure": "operations_support@mozilla.com",
        "Notification_Channel": "{{page.NOTIFICATION_CHANNEL}}",
    }
    data = {
        "ERROR_CODE": "ERROR_CODE_123456",
        "NOTIFICATION_CHANNEL": "NOTIFICATION_CHANNEL_123456",
    }
    rendered_content = {
        "Error_Code": "ERROR_CODE_123456",
        "Alert_Condition": "System was not able to do expected operation.",
        "Severity": "High",
        "Alert_Message": "Could not perform expected operation. This could result in duplicate entries.",
        "Recipient": "#operation-channel",
        "Suggested_Actions": "Forward Alert to Respective Team",
        "Escalation_Procedure": "operations_support@mozilla.com",
        "Notification_Channel": "NOTIFICATION_CHANNEL_123456",
    }
    tempf = create_temp_file_from_url(file_content=json.dumps(content))
    directory = os.path.dirname(tempf.name)
    file_path = str(tempf.name)
    error_code_as_file_name = os.path.basename(file_path)
    error_code_as_file_name_without_extentions = os.path.splitext(
        error_code_as_file_name
    )[0]
    alert_utils = AlertUtils(directory)
    rendered_template = alert_utils.render_alert_template(
        error_code=error_code_as_file_name_without_extentions, data=data
    )
    assert rendered_content == rendered_template


def create_temp_file_from_url(file_content):
    temp_file = tempfile.NamedTemporaryFile(
        mode="w+t", delete=False, suffix=".json", prefix=os.path.basename(__file__)
    )
    temp_file.write(file_content)
    temp_file.close()
    return temp_file
