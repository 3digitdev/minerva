import os
import sys
import json
from json import JSONDecodeError


def load_config():
    try:
        with open("minerva_config.json") as cfg:
            config = json.load(cfg)
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
