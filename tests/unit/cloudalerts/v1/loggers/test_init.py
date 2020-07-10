# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


def test__init__():
    from cloudalerts.v1.loggers import __all__

    expected = ["AlertLogger", "CloudLogging"]
    assert expected == __all__
