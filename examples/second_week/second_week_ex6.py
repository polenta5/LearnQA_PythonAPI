import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect")
redirect_history = response.history
print(f"Количество редиректов {len(list(redirect_history))}")

last_url = response.url
print(f"Итоговый урл {last_url}")