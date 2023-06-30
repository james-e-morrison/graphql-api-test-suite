from utils.call_api import post_to_api


def remove_all_roles() -> int :
    '''
    Utility function to remove all roles from the API. USE WITH CAUTION!
    '''

    query = '''
            query{
                Roles{
                    id
                    }
                }
    '''

    roles = post_to_api(payload={"query": query}).json()

    query = '''
            mutation($id: Int!){
            RoleDeleteOne(id: $id){
                affected
            }
            }
    '''

    variables = {
        "id": 0
    }

    removed_count = 0
    if roles['data']['Roles']:
        removed_count = len(roles['data']['Roles'])
        for role in roles['data']['Roles']:
            variables['id'] = int(role['id'])

            payload = {
                "query": query,
                "variables": variables
            }

            post_to_api(payload=payload)
    
    return removed_count


def remove_all_skills() -> int:
    '''
    Utility function to remove all skills from the API. USE WITH CAUTION!
    '''

    query = '''
            query{
                Skills{
                    id
                    }
                }
    '''

    roles = post_to_api(payload={"query": query}).json()

    query = '''
            mutation($id: Int!){
            SkillDeleteOne(id: $id){
                affected
            }
            }
    '''

    variables = {
        "id": 0
    }

    removed_count = 0
    if roles['data']['Skills']:
        removed_count = len(roles['data']['Skills'])
        for role in roles['data']['Skills']:
            variables['id'] = int(role['id'])

            payload = {
                "query": query,
                "variables": variables
            }

            post_to_api(payload=payload)

    
    return removed_count


def remove_role(id: int) -> None:
    '''
    Utility function to remove single role.
    '''

    query = '''
        mutation($id: Int!){
            RoleDeleteOne(id: $id){
                affected
            }
        }
    '''

    payload = {
        "query": query,
        "variables": {
            "id": id
        }
    }

    post_to_api(payload=payload, log=False)


def remove_skill(id: int) -> None:
    '''
    Utility function to remove single skill.
    '''

    query = '''
        mutation($id: Int!){
            SkillDeleteOne(id: $id){
                affected
            }
        }
    '''

    payload = {
        "query": query,
        "variables": {
            "id": id
        }
    }

    post_to_api(payload=payload)
