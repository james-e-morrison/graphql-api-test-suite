import requests
import logging
import datetime


ts = datetime.datetime.now()
ls = ts.strftime("%d-%b-%Y %H-%M-%S")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    #filename=ls + '_requests.log',
    filemode='w'
)


def post_to_api(payload, headers=None, log=False):
    """Perform the api call
    :return the api response
    """

    url = 'https://sz-sdet-task.herokuapp.com/graphql'
    response = requests.post(url, json=payload)
    if log: logging.info([response.request.headers, response.request.body, response.json()])
    response_data = response.json()
    return response
