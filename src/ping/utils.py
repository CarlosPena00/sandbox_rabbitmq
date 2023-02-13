import json

def json_to_bytes(j) -> bytes:
    return str.encode(json.dumps(j))


def bytes_to_json(b):
    return json.loads(b.decode())
