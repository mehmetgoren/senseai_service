import json
from types import SimpleNamespace


def deserialize_json(json_str, result):
    simple_namespace = json.loads(json_str, object_hook=lambda d: SimpleNamespace(**d))
    result.__dict__.update(simple_namespace.__dict__)
    return result
