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


def verify_datetime(request_datetime: str, response_datetime: str, time_diff = 0):
    '''
    Ensure the datetime returned in the api matches the request datetime
    '''
    request_datetime = convert_datetime(request_datetime)
    date_pattern = r'^\d{1,9}Z$'
    date_parts = response_datetime.split(".")

    # allow up to a 1 second difference in time due to slow server. During high load this may (correctly) fail
    request_datetime =  datetime.strptime(request_datetime, "%Y-%m-%dT%H:%M:%S")
    date_parts[0] = datetime.strptime(date_parts[0], "%Y-%m-%dT%H:%M:%S") # remove microseconds from api datetime
    #print(date_parts[0], request_datetime, request_datetime + timedelta(seconds=2))
    time_diff = date_parts[0] - request_datetime
    if not date_parts[0] >= request_datetime - timedelta(seconds=1):
        #raise ValueError(date_parts[0], request_datetime)
        raise ValueError(f"Datetime returned by the API was too distant from expected (Request time). Request time: {date_parts[0]}, API time: {request_datetime}")
    if not date_parts[0] <= (request_datetime + timedelta(seconds=1)):
        raise ValueError(f"Datetime returned by the API was too distant from expected (Request time). Request time: {date_parts[0]}, API time: {request_datetime}")
        
    assert re.match(date_pattern, date_parts[1]) != None


def compare_json(json1: dict, json2: dict) -> bool:
    '''
    Recursively compare that every object and key-value pair in the first json string is 
    present in the second. This is not a complete match but a programic way to check our 
    expected values are present within a second json string.
    '''

    if isinstance(json1, dict) and isinstance(json2, dict):
        for key in json1.keys():
            if key not in json2:
                raise ValueError(f"Expected key missing in response. Missing key: {key}")

            if not compare_json(json1[key], json2[key]):
                raise ValueError(f"Expected value mismatch. Expected: {key} = {json1[key]}, Actual: {key} = {json2[key]}")

    elif isinstance(json1, list) and isinstance(json2, list):
        if len(json1) != len(json2):
            raise ValueError(f"List {json1} was not the epxected length. Expected length: {len(json1)}, Actual length: {len(json2)}")
        for item1, item2 in zip(json1, json2):
            if not compare_json(item1, item2):
                return False

    else:
        if json1 != json2:
            raise ValueError(f"Expected json '{json1}' does not match actual json: '{json2}'")

    return True


def validate_json(data: str, schema_name: str):
    #data = json.loads(data)
    schema = json_schema_loader(schema_name)
    #jsonschema.validate(data, schema)
    try:
        jsonschema.validate(data, schema)
    except jsonschema.exceptions.ValidationError as e:
        raise jsonschema.exceptions.ValidationError(f"JSON data failed schema validation with error message: {e.message}. Path: {e.path}")
