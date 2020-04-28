Feature: Alerting

  Scenario: Alert using a template and replacing values (AlertUtils.alert_error_code)
    Given the client logger is Google
    Given error code folder tests/resources/error_codes/
    When we alert
      | key                  | value        |
      | ERROR_CODE           | E000010_test |
      | NOTIFICATION_CHANNEL | achannel     |
    Then template is set with
      | key                  | value                                                                             |
      | Error_Code           | E000010_test                                                                      |
      | Notification_Channel | achannel                                                                          |
      | Alert_Condition      | System was not able to do expected operation.                            |
      | Severity             | High                                                                              |
      | Alert_Message        | Could not perform expected operation. This could result in duplicate entries. |
      | Recipient            | #operation-channel                                                                          |
      | Suggested_Actions    | Forward Alert to Respective Team                                                  |
      | Escalation_Procedure | operations_support@mozilla.com                                                 |

  Scenario: Alert using a template and NOT replacing values (AlertUtils.get_alerting_info)
    Given the client logger is Google
    Given error code folder tests/resources/error_codes/
    When we alert E000011_test
    Then template is set with
      | key                  | value                       |
      | Error_Code           | ERROR_CODE_123456           |
      | Notification_Channel | NOTIFICATION_CHANNEL_123456 |
      | Alert_Condition      | System was not able to insert a consumed file.                            |
      | Severity             | High                                                                              |
      | Alert_Message        | Could not insert a consumed file. This could result in duplicate entries. |
      | Recipient            | #operation-channel                                                                          |
      | Suggested_Actions    | Forward Alert to Respective Team                                                  |
      | Escalation_Procedure | operations_support@mozilla.com                                                            |
