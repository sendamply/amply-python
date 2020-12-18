""" Amply exceptions """

import requests

class APIException(Exception):
    """Generic API exception"""

    def __init__(self, response):
        """Generic API exception"""

        try:
            super().__init__('An error occurred while making an API request')
        except TypeError:
            super(APIException, self).__init__('An error occurred while making an API request')

        self.status = response.status_code
        self.text = requests.status_codes._codes[self.status][0]

class ValidationException(Exception):
    """Validation exception"""
    def __init__(self, errors):
        """Validation exception"""

        try:
            super().__init__('A validation error occurred while making an API request')
        except TypeError:
            super(ValidationException, self).__init__('A validation error occurred while making an API request')

        self.errors = errors

class ResourceNotFoundException(Exception):
    """ResourceNotFound exception"""

    def __init__(self, errors):
        """ResourceNotFound exception"""

        try:
            super().__init__('The resource was not found while making an API request')
        except TypeError:
            super(ResourceNotFoundException, self).__init__('The resource was not found while making an API request')

        self.errors = errors
