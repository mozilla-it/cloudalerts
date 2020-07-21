# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import json
from typing import Dict

import jinja2
from jinja2 import Environment
from jinja2 import select_autoescape


class AlertUtils:
    errors: Dict[str, Dict] = dict()
    path_to_err_templates: str = None
    initialized: bool = False

    @staticmethod
    def initialize(path_to_err_templates: str):
        AlertUtils.path_to_err_templates = path_to_err_templates
        AlertUtils.initialized = True

    @staticmethod
    def reset():
        AlertUtils.errors = dict()
        AlertUtils.initialized = False
        AlertUtils.path_to_err_templates = None

    @staticmethod
    def get_number_of_errors() -> int:
        AlertUtils.confirm_initialization()
        return len(AlertUtils.errors)

    @staticmethod
    def confirm_initialization():
        if AlertUtils.initialized is False:
            raise Exception(
                "You must invoke AlertUtils.initialize with the appropriate parameters"
            )

    @staticmethod
    def __load_error_code(error_code) -> Dict:
        AlertUtils.confirm_initialization()

        with open(
            f"{AlertUtils.path_to_err_templates}/{error_code}.json", "r"
        ) as err_code_file:
            return json.loads(err_code_file.read())

    @staticmethod
    def get_alerting_info(error_code: str) -> Dict:
        """
        The error code file which contains the response.
        :param error_code: the error
        :return:
        """
        AlertUtils.confirm_initialization()

        if error_code in dict.keys(AlertUtils.errors):
            return AlertUtils.errors.get(error_code)

        AlertUtils.errors.update(
            {error_code: AlertUtils.__load_error_code(error_code=error_code)}
        )
        return AlertUtils.errors.get(error_code)

    @staticmethod
    def get_alerting_info_parameterize(error_code: str, data: Dict) -> Dict:
        """
        The error code is the template that will be loaded and the data is the parameters that will be replaced in the
        template. The data is a json structure built in memory.
        :param error_code: the template
        :param data: the data for the template
        :return: the final file after inserting data into template
        """
        AlertUtils.confirm_initialization()

        env = Environment(
            loader=jinja2.FileSystemLoader(AlertUtils.path_to_err_templates),
            autoescape=select_autoescape(["json"]),
        )
        env.filters["jsonify"] = json.dumps
        commmon_path = error_code + ".json"
        common_template = env.get_template(commmon_path)
        render = common_template.render(page=data)
        return json.loads(render)
