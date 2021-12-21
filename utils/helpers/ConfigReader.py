from pathlib import Path

import yaml


def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent


class Config:

    def __init__(self, config):
        self.config = config

    def get(self):
        self._read_application_yml()
        return self.find_config()

    def find_config(self):
        tokens = self.config.split(".")
        current_structure = self.yml
        value = None
        for token in tokens:
            if token in current_structure:
                value = current_structure[token]
                current_structure = current_structure[token]
        return value

    def _read_application_yml(self):
        with open("/".join((str(get_project_root()), 'application.yml')), "r") as stream:
            try:
                self.yml = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
