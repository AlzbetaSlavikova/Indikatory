import requests
import json
response = requests.get('https://transparency.entsog.eu/api/v1/operators?limit=-1')
data = json.loads(response.text)

seznam = [x['operatorLabel'] for x in data['operators']]


print(sorted(seznam))