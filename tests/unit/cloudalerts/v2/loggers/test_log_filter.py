# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import datetime

import pytest

from cloudalerts.v2.loggers.log_filter import censor_event_dict
from cloudalerts.v2.loggers.log_filter import censor_header

single_censorable_value_event_dictionary = {
    "a": "b",
    "event": "goodbye",
    "log_level": "info",
    "foo": {"bar": "baz"},
    "headers": {"X-Forwarded-For": "Mozilla"},
}

multiple_censorable_value_event_dictionary = {
    "a": "b",
    "event": "goodbye",
    "log_level": "info",
    "foo": {"bar": "baz"},
    "headers": {"Authorization": "authorization_secret", "X-Forwarded-For": "Mozilla"},
}

single_censorable_value_event_expected_dictionary = {
    "a": "b",
    "event": "goodbye",
    "log_level": "info",
    "foo": {"bar": "baz"},
    "headers": {"X-Forwarded-For": "*CENSORED*"},
}

multiple_censorable_value_event_expected_dictionary = {
    "a": "b",
    "event": "goodbye",
    "log_level": "info",
    "foo": {"bar": "baz"},
    "headers": {"Authorization": "*CENSORED*", "X-Forwarded-For": "*CENSORED*"},
}


def test_filter_msg_given_empty_event_dictionary():
    event_dict = {}
    censored_event_dict = censor_event_dict(event_dict)
    assert censored_event_dict is event_dict


def test_bad_param():
    event_dict = []
    with pytest.raises(AttributeError):
        assert censor_event_dict(event_dict)


def test_filter_msg_given_no_event_dictionary():
    event_dict = None
    with pytest.raises(AttributeError):
        censor_event_dict(event_dict)


def test_filter_msg_given_event_dictionary_without_censorable_values():
    event_dict = {"timestamp": datetime.datetime.utcnow()}
    censored_event_dict = censor_event_dict(event_dict)
    assert censored_event_dict == event_dict


def test_filter_msg_given_event_dictionary_with_one_censorable_values():
    censored_event_dict = censor_event_dict(single_censorable_value_event_dictionary)
    assert censored_event_dict == single_censorable_value_event_expected_dictionary


def test_filter_msg_given_event_dictionary_with_many_censorable_values():
    censored_event_dict = censor_event_dict(multiple_censorable_value_event_dictionary)
    assert censored_event_dict == multiple_censorable_value_event_expected_dictionary


def test_censor_header_with_empty_dictionary():
    assert censor_header("logger", "method_name", {}) == dict()


def test_censor_header_with_no_dictionary():
    with pytest.raises(AttributeError):
        censor_header("logger", "method_name", None)


def test_censor_header_given_event_dictionary_without_censorable_values():
    event_dict = {"timestamp": datetime.datetime.utcnow()}
    censored_event_dict = censor_header("logger", "method_name", event_dict)
    assert censored_event_dict == event_dict


def test_censor_header_given_event_dictionary_with_one_censorable_values():
    censored_event_dict = censor_header(
        "logger", "method_name", single_censorable_value_event_dictionary
    )
    assert censored_event_dict == single_censorable_value_event_expected_dictionary


def test_censor_header_given_event_dictionary_with_many_censorable_values():
    censored_event_dict = censor_header(
        "logger", "method_name", multiple_censorable_value_event_dictionary
    )
    assert censored_event_dict == multiple_censorable_value_event_expected_dictionary
