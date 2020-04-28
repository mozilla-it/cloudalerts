# cloud-alerts

A github repo for cloud alerting through Stackdriver.

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

```
**[Initialization should only happen once. ]**
AlertUtils.initialize(
               path_to_err_templates = <path_to_err_templates/>
              )

**[Get alerting info]**
alert_dict = AlertUtils.get_alerting_info(<error_code/>)

**[Get template alert filled with data provided]**
alert_dict = AlertUtils.get_alerting_info_parameterize(<error_code/>, <data/>)
```

```
**[Initialization should only happen once. ]**

from cloudalerts.alerts import AlertUtils
AlertUtils.initialize("LOOK AT THE EXAMPLE ABOVE")
AlertUtils.get_alerting_info("error_code")
>>> {'key1': 'value1', 'key2': 'value2'}
AlertUtils.get_alerting_info_parameterize("error_code",{"key_to_replace":"value_for_replacement"})
>>> {'key_non_template': 'same_value', 'key_template': 'injected new value into key - value_for_replacement'}
```

```
**[Initialization should only happen once. ]**

from cloudalerts.cloud_loggers import CloudLogging
logger = CloudLogging.get_logger()
logger.log_struct_message("Error message")
>>> sending struct payload with MESSAGE as the provided messaged to the cloud client logger
logger.log_alert_message("Error message")
>>> sending struct payload with MESSAGE as the provided messaged to the cloud client logger

logger.log_struct(AlertUtils.get_alerting_info("error_code"))
>>> sending struct payload with alert dict being the provided payload to the cloud client logger
logger.log_alert_info(AlertUtils.get_alerting_info("error_code"))
>>> sending struct payload with alert dict being the provided payload to the cloud client logger
logger.log_alert_by_error_code("error_code")
>>> sending struct payload with alert dict being the provided payload to the cloud client logger
```
