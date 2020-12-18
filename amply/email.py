"""Send an email"""

from .helpers.email import EmailHelper

class Email(object):
    """Create the email"""

    def __init__(self, client):
        """Create the email"""

        self.client = client
        self.email_helper = EmailHelper()

    def create(self, data):
        """Send the email"""

        parsed_data = self.email_helper.parsed_data(data)
        self.client.post('/email', parsed_data)
