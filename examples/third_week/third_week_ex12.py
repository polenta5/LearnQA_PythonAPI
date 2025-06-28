import requests

class TestHeaders:
    def test_get_headers_name(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_header")
        response_headers = {}
        response_headers.update(response.headers)
        print(f"Response have headers: {response_headers}")
        assert len(response_headers) > 0, "No headers in response"
