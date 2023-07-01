import pytest, re
from utils.test_utils import convert_datetime, validate_json, verify_datetime, verify_api_response
from utils.call_api import post_to_api
from datetime import datetime


def test_role_create_one(cleanup, test_data):
    '''Test the RoleCreateOne mutation.'''

    resp = post_to_api(payload={"query": test_data['payload']})
    print(resp.text)
    r_json = resp.json()
    cleanup['roles'].append(r_json['data']['RoleCreateOne']['id'])
    assert resp.status_code == test_data['expected-status-code']
    

    # check the returned json contains all the expected values
    assert verify_api_response(test_data['expected-response'], r_json)

    if 'createdAt' in test_data['expected-response']['data']['RoleCreateOne']:
        verify_datetime(resp.headers['Date'], r_json['data']['RoleCreateOne']['createdAt'])
    if 'updatedAt' in test_data['expected-response']['data']['RoleCreateOne']:
        verify_datetime(resp.headers['Date'], r_json['data']['RoleCreateOne']['updatedAt'])

    # if the test includes a schema then validate the api response against it
    if 'schema' in test_data:
        validate_json(r_json, test_data['schema'])


def test_end_to_end(test_data, cleanup):
    # create role
    resp = post_to_api(payload={"query": test_data['create-role']})
    cleanup['roles'].append(resp.json()['data']['RoleCreateOne']['id']) # hold the ids for deletion via the post-test cleanup

    # create skills
    for skill in test_data['skills']:
        print(test_data['skills'][skill])
        original_string = test_data['skills'][skill]
        skill_s = re.search('\"(.*?)\"', original_string).group(1)
        replacement_skill = skill_s + "_" + datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        replacement_string = test_data['skills'][skill].replace(skill_s, replacement_skill)
        print(replacement_string)
        resp = post_to_api(payload={"query": replacement_string})
        print(resp.json())
        cleanup['skills'].append(resp.json()['data']['SkillCreateOne']['id'])
    
    # create role skill
    payload = {
    "query": test_data['payload'],
    "variables": {
        "role_id": cleanup['roles'][0] 
    }
    }

    for index, id in enumerate(cleanup['skills']):
        skill_var = 'skill_id' + str(index+1)
        payload['variables'][skill_var] = id

    print(payload)
    resp = post_to_api(payload=payload)
    print(resp.text)

    assert resp.status_code == test_data['expected-status-code']
    r_json = resp.json()
    assert verify_api_response(test_data['expected-response'], r_json)
