import requests

response = requests.post('http://127.0.0.1:8000/nodes/drain/node1/')

print(response.json())