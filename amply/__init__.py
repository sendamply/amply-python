from .client import *
from .email import *
from .version import __version__

client = Client()
email = Email(client)

def set_access_token(token):
    client.set_access_token(token)
