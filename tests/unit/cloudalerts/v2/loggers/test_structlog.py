# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from cloudalerts.v2.loggers.structlog import event_uppercase


def test_event_uppercase():
    event_dict = {"event": "lower"}
    expected_dict = {"event": "LOWER"}
    actual_dict = event_uppercase(None, None, event_dict)
    assert expected_dict == actual_dict
