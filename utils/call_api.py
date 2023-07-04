import requests


def post_to_api(payload):
    """Perform the api call
    :return the api http response
    """

    url = 'https://sz-sdet-task.herokuapp.com/graphql'
    return requests.post(url, json=payload)
