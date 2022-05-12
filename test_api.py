### https://djoser.readthedocs.io/en/latest/sample_usage.html
### https://djoser.readthedocs.io/en/latest/base_endpoints.html

import pprint
import json
import requests
from requests.auth import HTTPBasicAuth


if __name__ == "__main__":

    API_ROOT = 'http://localhost:8000/'

    data = {"username": "testuser",
            "password": "alpine123"}

    # create user
    print('Creating user')
    res = requests.post(API_ROOT + 'auth/users/', data=data)

    # log in & retrieve token
    print('Retrieving token')
    res = requests.post(API_ROOT + 'auth/token/login/', data=data)
    token = json.loads(res.text)['auth_token']
    auth_header = {"Authorization": f"Token {token}"}
    print(token)

    # test get request
    # res = requests.get(API_ROOT + 'api/v1/recordings/', headers=auth_header)
    # print(res.text)

    # test post request
    print('Sending test data')
    post_data = {
        "name": "Puppies",
        "get_timestamps": True,
        "words": "puppy, puppies, mother"
    }

    files = {"audio_file": open('./audio_samples/puppy.mp3', 'rb')}

    res = requests.post(API_ROOT + 'api/v1/recordings/',
                        data=post_data, 
                        headers=auth_header, 
                        files=files
                        )

    try:
        pprint.pprint(json.loads(res.text))
    except AttributeError:
        print(res.status_code)

    # delete user
    print('deleting user')
    res = requests.delete(API_ROOT + 'auth/users/me/', headers=auth_header, data={'current_password': data['password']})
    print("execution finished")