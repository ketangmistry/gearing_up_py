import io
import os
import yaml


def get_yaml_object_from_file(relative_file_name: str):
    this_dir = os.path.dirname(__file__)
    absolute_path_to_file = os.path.join(this_dir, relative_file_name)

    with io.open(absolute_path_to_file, 'r') as stream:
        yaml_object = yaml.safe_load(stream)

    return yaml_object
