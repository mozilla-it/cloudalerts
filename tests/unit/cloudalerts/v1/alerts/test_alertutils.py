# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import pytest

ERROR_TEMPLATES = "tests/resources/error_codes/"


def test_alertutils_import():
    from cloudalerts.v1.alerts import __all__

    expected = ["AlertUtils"]
    assert expected == __all__


def test_more():
    from cloudalerts.v1.alerts import AlertUtils

    assert AlertUtils.initialized == False
    AlertUtils.initialize(ERROR_TEMPLATES)
    assert AlertUtils.initialized == True
    assert AlertUtils.path_to_err_templates == ERROR_TEMPLATES

    AlertUtils.reset()
    assert AlertUtils.initialized == False
    assert AlertUtils.path_to_err_templates == None

    with pytest.raises(Exception):
        assert AlertUtils.confirm_initialization()

    AlertUtils.initialize(ERROR_TEMPLATES)
    assert AlertUtils.get_number_of_errors() == 0

    # not loaded...
    alert = AlertUtils.get_alerting_info("E000010_test")
    assert type(alert) is dict
    # loaded...
    alert = AlertUtils.get_alerting_info("E000010_test")
    assert type(alert) is dict
