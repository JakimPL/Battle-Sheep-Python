import json


class Config:
    def __init__(self, key=None):
        with open("config.json") as file:
            data = json.load(file)
            self._data = data[key] if key else data

    def __getitem__(self, key):
        return self._data[key]
