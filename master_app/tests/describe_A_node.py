import requests

response = requests.get('http://127.0.0.1:8000/nodes/describe/node1/')

print(response.json())