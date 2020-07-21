# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

CENSORED_EVENT_VALUES_BY_EVENT_KEY = {
    "headers": ["Authorization", "X-Forwarded-For"],
    "multiValueHeaders": ["Authorization"],
}


def censor_event_dict(event_dict):
    if event_dict == dict():
        return event_dict
    for event_key, event_values in CENSORED_EVENT_VALUES_BY_EVENT_KEY.items():
        _event_key = event_dict.get(event_key)
        if _event_key:
            for event_value in event_values:
                _event_value = _event_key.get(event_value)
                if _event_key and _event_value:
                    event_dict[event_key][event_value] = "*CENSORED*"
    return event_dict


def censor_header(logger, method_name, event_dict):
    return censor_event_dict(event_dict)
