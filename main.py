from src.YAMLReader import *
from src.Config import *
from pprint import pprint

if __name__ == "__main__":
    file = "cargo"
    data = read_yaml(data_path() + file + ".yml")
    json_write(file, data)