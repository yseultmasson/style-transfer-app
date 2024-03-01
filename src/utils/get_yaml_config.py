"""Get yaml configuration."""

import os
import yaml


def import_yaml_config(filename: str = "configuration/config.yaml") -> dict:
    dict_config = {}
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as stream:
            dict_config = yaml.safe_load(stream)
    return dict_config
