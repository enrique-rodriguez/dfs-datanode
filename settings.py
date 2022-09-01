import json
from pathlib import Path


def get_config():
    with open("conf.json", "r") as f:
        config = json.load(f)
    
    config["basedir"] = str(Path(__file__).resolve().parent)
    
    return config