from dataclasses import asdict


def serialize_dataclass(data):
    if type(data) is list:
        return [
            serialize_dataclass(item)
            for item in data
        ]
    return asdict(data)
