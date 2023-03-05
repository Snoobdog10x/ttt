import os
import yaml

CONFIG_FILE = "config"


def _read_config_file(path):
    with open(path, 'r') as stream:
        try:
            data = yaml.safe_load(stream)
            return data
        except yaml.YAMLError as exc:
            print(exc)
            return {}


def get_enums_from_config(path):
    config = _read_config_file(path)
    if "enums" not in config or config["enums"] is None:
        return []
    return config["enums"]


def get_arguments_from_config(path):
    config = _read_config_file(path)
    if "arguments" not in config or config["arguments"] is None:
        return []
    return config["arguments"]


def create_path(path):
    if not check_file_exist(path):
        os.makedirs(path)


def write_file(path, output):
    with open(path, 'w') as file:
        file.write(output)
        file.close()


def check_file_exist(path):
    return os.path.exists(path)


def extract_file_name_from_config_file(path: str):
    paths = path.split('/')
    return paths[-1].replace(".yaml", "")


def to_camel_case(file_name: str, capitalize_first_char: bool = True):
    words = file_name.split('_')
    # Capitalize the first letter of each word
    if capitalize_first_char:
        capitalized_words = [word.capitalize() for word in words]
    else:
        capitalized_words = [[words[0]] + [word.capitalize() for word in words[1:]]]
    # Join the capitalized words together
    return ''.join(capitalized_words)


def get_all_config_file():
    file_paths = []
    for root, dirs, files in os.walk(CONFIG_FILE):
        for file_name in files:
            if file_name.endswith('.yaml'):
                file_path = os.path.join(root, file_name)
                file_paths.append(file_path)
    return file_paths
