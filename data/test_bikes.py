import bikes


def test_get_yaml_from_file():
    relative_file_name = 'bikes.yaml'
    yaml_object = bikes.get_yaml_object_from_file(relative_file_name)
    assert len(yaml_object['bikes']) > 0
