import json

from settings import PATH_TO_JSON


def read_json() -> list[dict]:
    with open(PATH_TO_JSON, mode='r', encoding='utf-8') as file:
        return json.load(file)
