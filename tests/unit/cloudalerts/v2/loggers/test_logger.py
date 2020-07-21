# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import pytest


def test_more(monkeypatch):
    from cloudalerts.v2.loggers import logger
    import cloudalerts.v2.loggers.structlog

    def mock_setup(*args, **kwargs):
        return None

    monkeypatch.setattr(cloudalerts.v2.loggers.logger, "setup", mock_setup)
    logger_inst = logger.get_log()
    assert (
        str(logger_inst)
        == "<BoundLoggerLazyProxy(logger=None, wrapper_class=None, processors=None, context_class=None, initial_values={}, logger_factory_args=())>"
    )
    logger_inst = logger.get_log()
    assert (
        str(logger_inst)
        == "<BoundLoggerLazyProxy(logger=None, wrapper_class=None, processors=None, context_class=None, initial_values={}, logger_factory_args=())>"
    )
