import os
import sys
import json
from json import JSONDecodeError
from typing import Any, Dict

CONFIG_SCHEMA = {
    # Format:  (<type>, <is_required>, <default_value>)
    "database": (str, False, "mongo"),
    "host": (str, False, "localhost"),
    "port": (int, False, 27017),
    "testing": (bool, False, False),
}


def _validate_config(config: Dict[str, Any]) -> Dict[str, Any]:
    errors = []
    valid_config = {}
    for key, schema in CONFIG_SCHEMA.items():
        val_type, is_required, default = schema
        if is_required:
            if key not in config:
                errors.append(f"Missing required entry '{key}' ({val_type.__name__})")
                continue
            value = config.get(key, default)
            if not isinstance(value, val_type):
                errors.append(
                    f"Entry '{key}' expected to be {val_type.__name__} -- was {type(value).__name__}"
                )
                continue
        else:
            value = config.get(key, default)
        valid_config[key] = value
    if errors:
        print("[Setup Errors]  Encounters one or more errors with your 'minerva_config.json'")
        print("----- Details -----")
        for err in errors:
            print(err)
        sys.exit(1)
    return valid_config


def load_config() -> Dict[str, Any]:
    try:
        with open("minerva_config.json") as cfg:
            config = _validate_config(json.load(cfg))

    except FileNotFoundError:
        print(
            f"[Setup Error]  You do not have a 'minerva_config.json' file located in [{os.getcwd()}]"
        )
        sys.exit(1)
    except JSONDecodeError as json_error:
        print("[Setup Error]  Your 'minerva_config.json' file is not valid JSON")
        print("----- Error Details -----")
        print(str(json_error))
        sys.exit(1)
    return config
