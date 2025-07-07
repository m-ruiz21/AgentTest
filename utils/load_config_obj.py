import json

def load_config_obj(path: str) -> dict:
    with open(path, "r") as f:
        conf = json.load(f)
    return conf