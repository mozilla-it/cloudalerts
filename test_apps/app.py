# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import logging

import structlog
from flask import Flask
from waitress import serve

from cloudalerts.v2.loggers.structlog import configure_structlog

configure_structlog()
app = Flask(__name__)
logger = structlog.get_logger()


@app.route("/")
def test():
    logger.info("app index request")
    return {"foo": "bar"}


if __name__ == "__main__":
    logger.info("app starting", app=app)
    serve(app, port=5000)
    logger.info("app exiting", app=app)
