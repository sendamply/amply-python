"""EmailAddress builder"""

class EmailAddress(object):
    """Parses an email address"""

    def __init__(self, email_data):
        """Parses an email address"""
        self.email = None
        self.name = None

        if isinstance(email_data, str):
            email_data = self.from_string(email_data)

        if not isinstance(email_data, dict):
            raise Exception('Expecting dict or string for email address data')

        name = email_data.get('name')
        email = email_data.get('email')

        self.set_email(email)
        self.set_name(name)


    @staticmethod
    def from_string(email_string):
        """Converts a string into a dictionary with name and email keys"""

        if not '<' in email_string:
            return {'name': None, 'email': email_string}

        name, email = email_string.split('<')

        name = name.strip()
        email = email.replace('>', '').strip()

        return {'name': name, 'email': email}

    def set_email(self, email):
        """Set the email instance variable"""
        if email is None:
            raise Exception('Must provide `email`')

        if not isinstance(email, str):
            raise Exception('String expected for `email`')

        self.email = email

    def set_name(self, name):
        """Set the name instance variable"""
        if name is None:
            return

        if not isinstance(name, str):
            raise Exception('String expected for `name`')

        self.name = name

    def to_json(self):
        """Convert object to easily parsable JSON dictionary"""

        json = {'email': self.email}

        if self.name != '':
            json['name'] = self.name

        return json

    @classmethod
    def create(cls, data):
        """Create EmailAddress object from different input data"""

        if isinstance(data, list):
            return [cls.create(email) for email in data if not not email]

        if isinstance(data, EmailAddress):
            return data

        return EmailAddress(data)
