import json
import requests





api_url = ' http://127.0.0.1:3000/post-requests'

json_object = {
        "title": "Test1", "input_text": "Hello, world. My name is Juan."
    }
res = requests.post(url=api_url, json=json_object)
print(res.status_code, res.reason, res.text)


