"""Send an email"""

from .helpers.email import EmailHelper

class Email(object):
    """Create the email"""

    def __init__(self, client):
        """Create the email"""

        self.client = client

    def create(self, data):
        """Send the email"""

        parsed_data = EmailHelper().parsed_data(data)
        self.client.post('/email', parsed_data)
