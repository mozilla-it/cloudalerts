![Cloud Build](https://storage.googleapis.com/dp2-admin-badges/builds/cloudalerts/branches/master.svg)


[![codecov](https://codecov.io/gh/mozilla-it/cloudalerts/branch/master/graph/badge.svg)](https://codecov.io/gh/mozilla-it/cloudalerts)


# cloud-alerts

A github repo for cloud alerting through cloud logging libraries (GCP: Stackdriver).

The Service component that scans for alerts and sends them to their recipient can be found here:
[Data-Alert-Sender](https://github.com/mozilla-it/data-alert-sender)

## Index

This template repo starts with some examples:
* [View All Docs](./docs/)
* [Developer Setup](./docs/developer_setup.md)
* [Testing Strategy](./docs/testing_strategy.md)

## Project Structure

The project is structured with the following in mind:

- docs/
    - Documentation around the project
- src/
    - Operational source code exists here
- tests/bdd/
    - BDD feature testing with Behave and Gherkin feature files
- tests/resources/
    - Resources of various files types, exist here

## Prerequisites

Please ensure following the [Developer Setup](./docs/developer_setup.md) before developing \
for this project to ensure correct environment setup.

It is also suggested to view the [others docs as well](./docs/).

# Example Usage

When using CloudAlerts there are two main components:
- CloudLogging
    - This is the logging component that can be used as a wrapper for connecting with Cloud Client logging solutions.
    - Currently the logging is set for Google to use the Stackdriver client
- AlertUtils
    - This component is used to create JSON blobs, either through jinja2 templatized JSON files
    - The initialization of this component for usability requires that you point to the file directory of the co-located code and error codes

 ### Structuring your Alerting Info through AlertUtils

Initialization is REQUIRED for alerting, as the alerts and errors are co-located with the code.
Please point this component to your directory of JSON error_codes.

Here's a brief example for interacting with AlertUtils and what to expect.
```
** [Initialization: only required once!] **
AlertUtils.initialize(
               path_to_err_templates = <path_to_err_templates/>
              )

** [Get alerting info from error code]**
alert_dict = AlertUtils.get_alerting_info(<error_code/>)

** [Get template alert filled with data provided]**
alert_dict = AlertUtils.get_alerting_info_parameterize(<template_error_code/>, <data/>)
```

Below you can find some example outputs when using AlertUtils to generate your JSON error codes in structured loggable values.
```
from cloudalerts.alerts.alert_utils import AlertUtils
AlertUtils.initialize("LOOK AT THE EXAMPLE ABOVE")
AlertUtils.get_alerting_info("error_code")
>>> {'key1': 'value1', 'key2': 'value2'}
AlertUtils.get_alerting_info_parameterize("error_code",{"key_to_replace":"value_for_replacement"})
>>> {'key_non_template': 'same_value', 'key_template': 'injected new value into key - value_for_replacement'}
```

### Logging to cloud clients with CloudLogging
CloudLogging requires that the necessary ENV vars be set for the chosen client logging solution.

For use with Stackdriver (on google cloud platform) we need to ensure correct ENV vars are set up
- Please view this setup guide: [Developer Setup](./docs/developer_setup.md)

**New way** for interacting with CloudLogging, "alert" methods to chain with AlertUtils.
- log_alert_message
    - Alerts the CloudLogger with the message/str provided
- log_alert_info
    - Takes a structured alert payload and sends it to the CloudLogger
- log_alert_by_error_code
    - Takes an error code, pulls that structured payload from AlertUtils then sends it to the CloudLogger
    - ...currently only supporting error blobs not requiring templatized injection.
```
from cloudalerts.cloud_loggers.alert_logging import CloudLogging
logger = CloudLogging.get_logger()
logger.log_alert_message("Error message")
>>> (sending struct payload with MESSAGE as the provided messaged to the cloud client logger)

logger.log_alert_info(AlertUtils.get_alerting_info("error_code"))
>>> sending struct payload with alert dict being the provided payload to the cloud client logger
logger.log_alert_by_error_code("error_code")
>>> sending struct payload with alert dict being the provided payload to the cloud client logger
```

**Old way** for interacting with CloudLogging, "alert" methods to chain with AlertUtils.
- log_struct_message
    - Alerts the CloudLogger with the message/str provided
- log_struct
    - Takes a structured alert payload and sends it to the CloudLogger
```
logger.log_struct_message("Error message")
>>> (sending struct payload with MESSAGE as the provided messaged to the cloud client logger)
logger.log_struct(AlertUtils.get_alerting_info("error_code"))
>>> sending struct payload with alert dict being the provided payload to the cloud client logger
```

### Thanks!

Thanks for using this repo. Please reach out if there are any complications or questions.
