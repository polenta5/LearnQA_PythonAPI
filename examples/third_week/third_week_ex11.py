import requests

class TestCookie:
    def test_get_cookie_name(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
        cookie_value = {}
        cookie_value.update(response.cookies)
        print(f"Response have cookie: {cookie_value}")
        assert len(cookie_value) > 0, "No cookie in response"
