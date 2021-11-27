import requests
from datetime import datetime, timedelta

from configparser import ConfigParser
config = ConfigParser()
config.read('config.ini')
token = config.get('auth', 'token')

URL = f'https://api.github.com/search/repository?q=is:public created:SINCE..UNTIL'
HEADERS = {'Authorization': 'token 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'}

since = datetime.today() - timedelta(days=30)  # Since 30 days ago
until = since + timedelta(days=1)   # Until 29 days ago

while until < datetime.today():
    day_url = URL.replace('SINCE', since.strftime(
        '%Y-%m-%dT%H:%M:%SZ')).replace('UNTIL', until.strftime('%Y-%m-%dT%H:%M:%SZ'))
    r = requests.get(day_url, headers=HEADERS)
    print(
        f'Repositories created between {since} and {until}: {r.json().get("total_count")}')

    # Update dates for the next search
    since = until
    until = since + timedelta(days=1)
