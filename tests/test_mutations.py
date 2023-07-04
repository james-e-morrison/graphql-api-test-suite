
from datetime import datetime
import re
from utils.test_utils import validate_json, verify_datetime, verify_api_response
from utils.call_api import post_to_api


def test_role_create_one(cleanup, test_data):
    '''Test the RoleCreateOne mutation.'''

    resp = post_to_api(payload={"query": test_data['payload']})
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


def test_rollskill_overwrite(test_data, cleanup):
    '''Test to test the RoleskillOverwrite mutation. This test first needs to create role and skills before
        generating the RoleskillOverwrite mutation before validating the API response.
    '''
    
    # create role
    resp = post_to_api(payload={"query": test_data['create-role']})
    r_json = resp.json()
    cleanup['roles'].append(r_json['data']['RoleCreateOne']['id']) # hold the ids for deletion via the post-test cleanup
 
    # create skills and ensure a unique name using timestamp
    for index, skill in enumerate(test_data['skills']):
        original_string = test_data['skills'][skill]
        skill_s = re.search('\"(.*?)\"', original_string).group(1)
        replacement_skill = skill_s + "_" + datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        replacement_string = test_data['skills'][skill].replace(skill_s, replacement_skill)
        resp = post_to_api(payload={"query": replacement_string})
        r_json = resp.json()
        cleanup['skills'].append(r_json['data']['SkillCreateOne']['id']) # hold the skill ids for deletion via the post-test cleanup
        # put the modified unique name back into test data
        test_data['expected-response']['data']['RoleSkillsOverwrite'][index]['skill']['name'] = replacement_skill
    
    
    # put the role and skill ids into the query
    payload = {
    "query": test_data['payload'],
    "variables": {
        "role_id": cleanup['roles'][0] 
        }
    }
    for index, id in enumerate(cleanup['skills']):
        skill_var = 'skill_id' + str(index+1)
        payload['variables'][skill_var] = id

    # finally, make the roleskilloverwrite call and verify the response
    resp = post_to_api(payload=payload)
    assert resp.status_code == test_data['expected-status-code']
    assert verify_api_response(test_data['expected-response'], resp.json())
