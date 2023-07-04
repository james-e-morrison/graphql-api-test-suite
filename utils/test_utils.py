from datetime import datetime, timedelta
import json, jsonschema, re
from utils.read_test_data import json_schema_loader


def convert_datetime(request_dt: str) -> str:
    '''
    Convert the date from a http request to the same format of the API to allow direct comparison.
    '''

    api_dt_format = '%Y-%m-%dT%H:%M:%S.%fZ'
    requests_dt_format = '%a, %d %b %Y %H:%M:%S %Z'

    # Convert the requests datetime string to the api format
    request_dt = datetime.strptime(request_dt, requests_dt_format)
    return request_dt.strftime(api_dt_format)[:-8]


def verify_datetime(request_datetime: str, response_datetime: str, t_diff = 1):
    '''
    Ensure the datetime returned in the api matches the request datetime
    '''
    request_datetime = convert_datetime(request_datetime)
    microsecs_pattern = r'^\d{1,9}Z$'
    date_parts = response_datetime.split(".")
    assert re.match(microsecs_pattern, date_parts[1]) is not None

    # allow up to a 1 second difference in time due to slow server. During high load this may (correctly) fail
    request_datetime =  datetime.strptime(request_datetime, "%Y-%m-%dT%H:%M:%S")
    date_parts[0] = datetime.strptime(date_parts[0], "%Y-%m-%dT%H:%M:%S") # remove microseconds from api datetime
    time_diff = date_parts[0] - request_datetime
    if not date_parts[0] >= request_datetime - timedelta(seconds=t_diff):
        #raise ValueError(date_parts[0], request_datetime)
        raise ValueError(f"Datetime returned by the API was too distant from expected (Request time). Request time: {date_parts[0]}, API time: {request_datetime}")
    if not date_parts[0] <= (request_datetime + timedelta(seconds=t_diff)):
        raise ValueError(f"Datetime returned by the API was too distant from expected (Request time). Request time: {date_parts[0]}, API time: {request_datetime}")


def verify_api_response(expected: dict, actual: dict) -> bool:
    '''Single function to both verify the expected values in a api response and check no addtional unexpected keys are
    prent in the api response'''
    compare_json(expected, actual)
    check_for_unexpected_keys(actual, expected)
    return True


def compare_json(expected: dict, actual: dict) -> bool:
    '''
    Recursively compare that every object and key-value pair in the first json string is 
    present in the second. This is not a complete match but a programic way to check our 
    expected values are present within a second json string.
    '''

    if isinstance(expected, dict) and isinstance(actual, dict):
        for key in expected.keys():
            if key not in actual:
                raise ValueError(f"Expected key missing in API response. Missing key: {key}")

            if not compare_json(expected[key], actual[key]):
                raise ValueError(f"Expected value mismatch. Expected: {key} = {expected[key]}, Actual: {key} = {actual[key]}")

    elif isinstance(expected, list) and isinstance(actual, list):
        if len(expected) == 0 and len(actual) != 0 or len(expected) != 0 and len(actual) == 0:
            assert expected == actual
        for item1, item2 in zip(expected, actual):
            if not compare_json(item1, item2):
                return False

    elif expected and '::FUNC::' in str(expected):
        eval(expected.replace('::FUNC::', ''))(actual)
    
    elif expected != actual:
        raise ValueError(f"Expected json value '{expected}' does not match actual value: '{actual}'")
    
    return True


def validate_id(id: int):
    assert isinstance(id, int)
    assert id < 10000000 # sanity check to ensure ID is not at a silly count

def validate_name(name: str):
    pass


def validate_datetime_format(dt: str):
    '''
    Ensure a datetime returned by the API follows the expected format
    '''
    microsecs_pattern = r'^\d{1,9}Z$'
    date_parts = dt.split(".")
    assert re.match(microsecs_pattern, date_parts[1]) != None
    datetime.strptime(date_parts[0], "%Y-%m-%dT%H:%M:%S")
        

def validate_json(data: str, schema_name: str):
    '''
    Validate the given json against a schema
    '''
    schema = json_schema_loader(schema_name)
    try:
        jsonschema.validate(data, schema)
    except jsonschema.exceptions.ValidationError as e:
        raise jsonschema.exceptions.ValidationError(f"JSON data failed schema validation with error message: {e.message}. Path: {e.path}")


def check_for_unexpected_keys(actual, expected):
    if isinstance(actual, dict) and isinstance(expected, dict):
        for key in actual.keys():
            if key not in expected:
                raise ValueError(f"Json key '{key}' that was returned in the API response was not explicitly checked for in the test data, suggesting this key should not be present.")

            # Recursively compare nested dictionaries
            if isinstance(actual[key], dict) and isinstance(expected[key], dict):
                if not check_for_unexpected_keys(actual[key], expected[key]):
                    raise ValueError(f"Json key '{key}' that was returned in the API response was not explicitly checked for in the test data, suggesting this key should not be present.")
            
            # Check if values are lists
            elif isinstance(actual[key], list) and isinstance(expected[key], list):
                if len(actual[key]) != len(expected[key]):
                    raise ValueError(f"Json key '{key}' has a different number of elements in the API response compared to the test data.")

                for item1, item2 in zip(actual[key], expected[key]):
                    if not check_for_unexpected_keys(item1, item2):
                        raise ValueError(f"Json key '{key}' has unexpected elements in the API response compared to the test data.")
    return True
