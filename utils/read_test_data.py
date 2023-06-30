import json
import os

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), '../resources/test-data/')
JSON_SCHEMA_DIR = os.path.join(os.path.dirname(__file__), '../resources/schemas/')


def read_test_data_json(file_name: str) -> dict:
    """Read a json file containing test data into mem as one block
    """
    file_name = os.path.join(TEST_DATA_DIR, file_name + '.json')
    with open(file_name, "r") as fil_descriptor:
        data = json.load(fil_descriptor)
        return data


def split_tests(data_file: str) -> tuple:
    """Split dict of tests into seperate tests and put each test into a tuple
        so as to be ready for pytest.
    """

    # now read in the test data file
    test_data = read_test_data_json(data_file)
    # finally, split the dict by test case ready for pytest
    split_test_data = []
    for tc_id, tst in test_data.items():
        split_test_data.append(test_data[tc_id])

    return tuple(split_test_data)


def get_test_ids(data_file: str) -> dict:
    """Get just the test ids and description of each test
        and ignore the test data. Used for pytest parameterization.
    """
    data = read_test_data_json(data_file)
    keys = []
    for key in data.keys():
        keys.append(key)
    return keys


def json_schema_loader(file_name):
    """Read json file as json object.
    """
    file_name = JSON_SCHEMA_DIR + file_name + ".json"
    with open(file_name, "r") as fil_descriptor:
        data = json.load(fil_descriptor)
        return data
