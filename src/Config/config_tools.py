import json
import toml
import os
import io

from dotenv import load_dotenv


# region JSON
def json_read(file):
    with io.open(data_path() + f"{file}.json", "r", encoding="utf8") as json_file:
        json_data = json.load(json_file)
    return json_data


def from_json(file, tag):
    json_data = json_read(file)
    return json_data[tag]


def json_write(file, content):
    with io.open(data_path() + f"{file}.json", "w", encoding="utf8") as json_file:
        json.dump(content, json_file, indent=2)
# endregion


# region TOML
def toml_read(file):
    with io.open(data_path() + f"{file}.toml", "r", encoding="utf8") as toml_file:
        toml_data = toml.load(toml_file)
    return toml_data


def from_toml(file, tag):
    toml_data = toml_read(file)
    return toml_data[tag]


def toml_write(file, content):
    with io.open(data_path() + f"{file}.toml", "w", encoding="utf8") as toml_file:
        toml.dump(content, toml_file)
# endregion


def env(key):
    load_dotenv(dotenv_path=data_path() + ".env")
    return os.getenv(key)


def data_path():
    return os.getcwd() + '/data/'