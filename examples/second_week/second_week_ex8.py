import requests
import json
import time

response1 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")
obj = json.loads(response1.text)
print(f"Token: {obj.get('token')}")
print(f"Seconds: {obj.get('seconds')}")

seconds_value = int(obj.get('seconds'))
token_value = obj.get('token')
token = {}
token.update({'token': token_value})

response2 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params=token)
print(response2.status_code)
print(response2.text)

time.sleep(seconds_value)

response3 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params=token)
print(response3.status_code)
print(response3.text)