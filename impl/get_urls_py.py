import requests
from requests.utils import quote
import json

from configparser import ConfigParser
config = ConfigParser()
config.read('config.ini')
token = config.get('auth', 'token')
url = "https://api.github.com"

gh_session = requests.Session()
gh_session.auth = (token, "x-oauth-basic")

keyword = "serverless"
interval = 20


# print(repos)
