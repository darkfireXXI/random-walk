import json

import requests

url = "http://0.0.0.0:50051"
# url = "http://0.0.0.0:50051/register"
# url = "http://127.0.0.1:50051/"

r = requests.get(url)
# payload = {"user_name": "user_name", "password": "password", "email": "email"}
# r = requests.post(url, data=json.dumps(payload))
print(r)
print(r.text)
# print(r.json())
