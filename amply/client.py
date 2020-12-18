"""This library allows you to quickly and easily use the Amply API v1 via Python"""

import json
import requests

from .exceptions import APIException, ValidationException, ResourceNotFoundException

class Client(object):
    """The Amply API Client"""

    DEFAULT_HEADERS = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    def __init__(self):
        """Construct the API object"""

        self.access_token = ''
        self.url = 'https://sendamply.com/api/v1'

    def set_access_token(self, token):
        """Set your access token"""

        self.access_token = token

    def post(self, path, body, options={}):
        """Send a POST request to the Amply API"""

        headers = {}

        headers.update(self.DEFAULT_HEADERS)
        headers.update(options.get('headers') or {})
        headers.update(self.auth_header() or {})

        url = '%s%s' %(self.url, path)
        response = requests.post(url, json.dumps(body), headers=headers)

        return self.check_response(response)

    def put(self, path, body, options={}):
        """Send a PUT request to the Amply API"""

        headers = {}

        headers.update(self.DEFAULT_HEADERS)
        headers.update(options.get('headers') or {})
        headers.update(self.auth_header() or {})

        url = '%s%s' %(self.url, path)
        response = requests.put(url, json.dumps(body), headers=headers)

        return self.check_response(response)

    def delete(self, path, body, options={}):
        """Send a DELETE request to the Amply API"""

        headers = {}

        headers.update(self.DEFAULT_HEADERS)
        headers.update(options.get('headers') or {})
        headers.update(self.auth_header() or {})

        url = '%s%s' %(self.url, path)
        response = requests.delete(url, json.dumps(body), headers=headers)

        return self.check_response(response)

    def auth_header(self):
        """Construct the Authorization: Bearer header"""

        return {'Authorization': 'Bearer %s' %(self.access_token)}

    def check_response(self, response):
        """Validate the API response"""

        status = response.status_code

        if status == 204:
            return
        elif status == 401 or status == 403:
            raise APIException(response)
        elif status == 404:
            json = response.json()
            raise ResourceNotFoundException(json.get('errors'))
        elif status == 422:
            json = response.json()
            raise ValidationException(json.get('errors'))
        elif status < 200 or status >= 300:
            text = response.text
            raise APIException(response)

        return response.json()
