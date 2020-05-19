from typing import Dict
import json
from jinja2 import Environment, select_autoescape
import jinja2


class Alerter:
    class __Alerter:
        def __init__(self, path_to_err_templates: str):
            self.path_to_err_templates = path_to_err_templates
            self.errors: Dict[str, Dict] = dict()

        def get_number_of_errors(self) -> int:
            return len(self.errors)

        def __load_error_code(self, error_code) -> Dict:
            with open(
                f"{self.path_to_err_templates}/{error_code}.json", "r"
            ) as err_code_file:
                return json.loads(err_code_file.read())

        def get_alerting_info(self, error_code: str) -> Dict:
            """
                The error code file which contains the response.
                :param error_code: the error
                :return:
                """
            if error_code in dict.keys(self.errors):
                self.__load_error_code(error_code=error_code)
                return self.errors.get(error_code)

            self.errors.update(
                {error_code: self.__load_error_code(error_code=error_code)}
            )
            return self.errors.get(error_code)

        def get_alerting_info_parameterize(self, error_code: str, data: Dict) -> Dict:
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
            commmon_path = error_code + ".json"
            common_template = env.get_template(commmon_path)
            render = common_template.render(page=data)
            return json.loads(render)

    __instance = None

    def __init__(self, path_to_err_templates: str = None):
        if not Alerter.__instance and path_to_err_templates is not None:
            Alerter.__instance = Alerter.__Alerter(
                path_to_err_templates=path_to_err_templates
            )

    def get_instance(self):
        return self.__instance
