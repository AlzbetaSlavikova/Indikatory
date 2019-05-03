import requests
import json
response = requests.get('https://transparency.entsog.eu/api/v1/connectionpoints?limit=-1')
data = json.loads(response.text)

seznam = [x['pointLabel'] for x in data['connectionpoints']]


print(sorted(seznam))