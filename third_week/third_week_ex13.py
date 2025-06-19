import requests
import pytest

class TestUserAgent:
    user_agent_values = [('Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'),
                         ('Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1'),
                         ('Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'),
                         ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0"'),
                         ('Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1')]
    exp_platform_values = [('Mobile'), ('Mobile'), ('Googlebot'), ('Web'), ('Mobile')]
    exp_browser_values = [('No'), ('Chrome'), ('Unknown'), ('Chrome'), ('No')]
    exp_device_values = [('Android'), ('iOS'), ('Unknown'), ('No'), ('Iphone')]

    @pytest.mark.parametrize('user_agent_value, exp_platform_value, exp_browser_value, exp_device_value',
                             zip(user_agent_values, exp_platform_values, exp_browser_values, exp_device_values))
    def test_user_agent_check(self, user_agent_value, exp_platform_value, exp_browser_value, exp_device_value):
        url = "https://playground.learnqa.ru/ajax/api/user_agent_check"
        headers_value = {"User-Agent": user_agent_value}

        response = requests.get(url, headers=headers_value)
        response_dict = response.json()
        response_platform = response_dict.get('platform')
        response_browser = response_dict.get('browser')
        response_device = response_dict.get('device')

        assert response_platform == exp_platform_value, f"For agent value {user_agent_value} received platform value {response_platform}. This doesn't match with expected platform value {exp_platform_value}"
        assert response_browser == exp_browser_value, f"For agent value {user_agent_value} received browser value {response_browser}. This doesn't match with expected browser value {exp_browser_value}"
        assert response_device == exp_device_value, f"For agent value {user_agent_value} received device value {response_device}. This doesn't match with expected device value {exp_device_value}"


