import pytest

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserRegister(BaseCase):

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = "vinkotov@example.com"
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"

    # Ex15.1 - Создание пользователя с некорректным email - без символа @
    def test_create_user_with_not_correct_email(self):
        email = "vinkotovexample.com"
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        expected_message = f"Invalid email format"
        actual_message = response.content.decode("utf-8")
        assert expected_message in actual_message, f"Unexpected error message: {actual_message}"

    # Ex15.1 - - Создание пользователя без указания одного из полей
    # - с помощью @parametrize необходимо проверить, что отсутствие любого параметра не дает зарегистрировать пользователя
    exclude_params = {
        ("no_password"),
        ("no_username"),
        ("no_firstName"),
        ("no_lastName"),
        ("no_email")
    }

    @pytest.mark.parametrize('condition', exclude_params)
    def test_register_without_one_parameter(self, condition):
        data = self.prepare_registration_data()
        del data[condition[3:]]

        response = MyRequests.post("/user/", data=data)

        expected_message = f"The following required params are missed: {condition[3:]}"
        actual_message = response.content.decode("utf-8")
        assert expected_message in actual_message, f"Unexpected error message: {actual_message}"

# Ex15.3 - Создание пользователя с очень коротким именем в один символ
    def test_register_with_one_symbol_name(self):
        data = self.prepare_registration_data()
        new_firstName = "a"
        data['firstName'] = new_firstName

        response = MyRequests.post("/user/", data=data)

        expected_message = f"The value of 'firstName' field is too short"
        actual_message = response.content.decode("utf-8")
        assert expected_message in actual_message, f"Unexpected error message: {actual_message}"

# Ex15.4 - Создание пользователя с очень длинным именем - длиннее 250 символов
    def test_register_with_too_long_name(self):
        data = self.prepare_registration_data()
        new_firstName = "Сквозь сумрак ночи свет луны струился нежно, озаряя тихий сад. Тень берёзы легла на тропинку, шепча старинную сказку забытых времён. Ветер колыхнул ветви, словно вторя мелодии звёзд."
        data['firstName'] = new_firstName

        response = MyRequests.post("/user/", data=data)

        expected_message = f"The value of 'firstName' field is too long"
        actual_message = response.content.decode("utf-8")
        assert expected_message in actual_message, f"Unexpected error message: {actual_message}"



