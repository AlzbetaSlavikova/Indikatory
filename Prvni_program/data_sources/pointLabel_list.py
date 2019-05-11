import requests
import json
response = requests.get('https://transparency.entsog.eu/api/v1/operatorpointdirections?limit=-1')
data = json.loads(response.text)

#seznam = [(x['pointLabel'], x['pointKey']) for x in data['connectionpoints']]
#print (data['pointLabel']), (data['pointKey'])

#print(data)
#print(sorted(seznam))

points_dict = list()

for x in data['operatorpointdirections']:
    hodnoty = {
        "pointKey": x['pointKey'],
        "pointLabel": x['pointLabel'],
        "operatorLabel": x['operatorLabel'],
        "operatorKey": x['operatorKey']
    }
    points_dict.append(hodnoty)


print(points_dict)