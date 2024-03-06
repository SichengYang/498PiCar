import requests
import json

response = requests.get("https://ec2-13-60-47-81.eu-north-1.compute.amazonaws.com/json.php", verify=False)

response_json = response.json()

print(response_json['type'])
print(response_json['x'])
print(response_json['y'])