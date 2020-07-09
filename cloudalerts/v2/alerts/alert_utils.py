# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json
import jinja2
from typing import Dict
from jinja2 import Environment, select_autoescape
from cachetools import cached, TTLCache


class AlertUtils:
    def __init__(self, path_to_err_templates: str):
        self.errors: Dict[str, Dict] = dict()
        self.path_to_err_templates = path_to_err_templates

    def add(self, error_key, error_value):
        self.errors[error_key] = error_value

    def acknowledge_errors(self):
        self.errors.clear()

    def get_length(self) -> int:
        return len(self.errors)

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def __load(self, error_code) -> Dict:
        with open(
            f"{self.path_to_err_templates}/{error_code}.json", "r"
        ) as err_code_file:
            return json.loads(err_code_file.read())

    @cached(cache=TTLCache(maxsize=1024, ttl=600))
    def get_error_details(self, error_code: str) -> Dict:
        """
        The error code file which contains the response.
        :param error_code: the error
        :return:
        """
        if error_code in dict.keys(self.errors):
            self.__load(error_code=error_code)
            return self.errors.get(error_code)

        self.errors.update({error_code: self.__load(error_code=error_code)})
        return self.errors.get(error_code)

    def render_alert_template(self, error_code: str, data: Dict) -> Dict:
        """
        The error code is the template that will be loaded and the data is the parameters that will be replaced in the
        template. The data is a json structure built in memory.
        :param error_code: the template
        :param data: the data for the template
        :return: the final file after inserting data into template
        """
        env = Environment(
            loader=jinja2.FileSystemLoader(self.path_to_err_templates),
            autoescape=select_autoescape(["json"]),
        )
        env.filters["jsonify"] = json.dumps
        render = env.get_template(error_code + ".json").render(page=data)
        return json.loads(render)
