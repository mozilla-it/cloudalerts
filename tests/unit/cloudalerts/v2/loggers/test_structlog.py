# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


def test_event_uppercase():
    from cloudalerts.v2.loggers.structlog import event_uppercase

    event_dict = {"event": "lower"}
    expected_dict = {"event": "LOWER"}
    actual_dict = event_uppercase(None, None, event_dict)
    assert expected_dict == actual_dict


def test_configure_structlog():
    from cloudalerts.v2.loggers.structlog import configure_structlog

    result = configure_structlog()
    assert result == None
