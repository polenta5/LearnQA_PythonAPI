import allure
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


@allure.epic("Edit user cases")
@allure.feature("Editing")
class TestUserEdit(BaseCase):
    @allure.story("Positive edit scenario")
    @allure.severity(allure.severity_level.MINOR)
    @allure.description("This test successfuly edit just created user")
    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, 'auth_sid')
        token = self.get_header(response2, 'x-csrf-token')

        # EDIT
        new_name = "Changed name"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            f"Wrong name of the user after edit"
        )

    # Ex17.1 - Попытаемся изменить данные пользователя, будучи неавторизованными
    @allure.story("Negative edit scenario")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("This test prohibits editing a user without an account")
    def test_negative_edit_user_without_auth(self):
        data = self.prepare_registration_data()
        response_1 = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response_1, 200)
        Assertions.assert_json_has_key(response_1, "id")

        email = data['email']
        first_name = data['firstName']
        password = data['password']
        user_id = self.get_json_value(response_1, "id")

        new_first_name = first_name + 'test'

        response_2 = MyRequests.put(
            f"/user/{user_id}",
            data={
                "firstName": new_first_name,
            }
        )

        Assertions.assert_code_status(response_2, 400)
        expected_message = f"Auth token not supplied"
        actual_message = response_2.content.decode("utf-8")
        assert expected_message in actual_message, f"Unexpected error message: {actual_message}"

    # Ex17.2 - Попытаемся изменить данные пользователя, будучи авторизованными другим пользователем
    @allure.story("Negative edit scenario")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("This test prevents editing a user when logged in as another user.")
    def test_negative_edit_user_with_auth_other_user(self):
        data = self.prepare_registration_data()
        response_1 = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response_1, 200)
        Assertions.assert_json_has_key(response_1, "id")

        response_2 = MyRequests.post("/user/login", data=data)
        auth_sid = self.get_cookie(response_2, 'auth_sid')
        token = self.get_header(response_2, 'x-csrf-token')

        data_2 = self.prepare_registration_data()
        response_2 = MyRequests.post("/user/", data=data_2)

        Assertions.assert_code_status(response_2, 200)
        Assertions.assert_json_has_key(response_2, "id")
        first_name_2 = data_2['firstName']
        new_first_name_2 = first_name_2 + 'test'
        user_id_2 = self.get_json_value(response_2, "id")

        response_3 = MyRequests.put(
            f"/user/{user_id_2}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_first_name_2}
        )

        Assertions.assert_code_status(response_3, 400)
        expected_message = f"This user can only edit their own data."
        actual_message = response_3.content.decode("utf-8")
        assert expected_message in actual_message, f"Unexpected error message: {actual_message}"

    # Ex17.3 - Попытаемся изменить email пользователя, будучи авторизованными тем же пользователем,
    # на новый email без символа @
    @allure.story("Negative edit scenario")
    @allure.severity(allure.severity_level.MINOR)
    @allure.description("The test checks the prohibition of changing the email to an address without @")
    def test_negative_edit_user_with_incorrect_email(self):
        data = self.prepare_registration_data()
        response_1 = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response_1, 200)
        Assertions.assert_json_has_key(response_1, "id")

        email = data['email']
        new_email = email.replace("@", "")
        password = data['password']
        user_id = self.get_json_value(response_1, "id")

        response_2 = MyRequests.post("/user/login", data={
            "email": email,
            "password": password,
        })

        auth_sid = self.get_cookie(response_2, 'auth_sid')
        token = self.get_header(response_2, 'x-csrf-token')

        response_3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": new_email}
        )

        Assertions.assert_code_status(response_3, 400)
        expected_message = f"Invalid email format"
        actual_message = response_3.content.decode("utf-8")
        assert expected_message in actual_message, f"Unexpected error message: {actual_message}"

    # Ex17.4 - - Попытаемся изменить firstName пользователя, будучи авторизованными тем же пользователем,
    # на очень короткое значение в один символ
    @allure.story("Negative edit scenario")
    @allure.severity(allure.severity_level.MINOR)
    @allure.description("The test checks the prohibition of changing the email to a name of 1 symbol")
    def test_negative_edit_user_with_incorrect_firstname(self):
        data = self.prepare_registration_data()
        response_1 = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response_1, 200)
        Assertions.assert_json_has_key(response_1, "id")

        first_name = data['firstName']
        new_first_name = first_name[0]
        password = data['password']
        email = data['email']
        user_id = self.get_json_value(response_1, "id")

        response_2 = MyRequests.post("/user/login", data={
            "email": email,
            "password": password,
        })

        auth_sid = self.get_cookie(response_2, 'auth_sid')
        token = self.get_header(response_2, 'x-csrf-token')

        response_3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_first_name}
        )

        Assertions.assert_code_status(response_3, 400)
        expected_message = f"The value for field `firstName` is too short"
        actual_message = response_3.content.decode("utf-8")
        assert expected_message in actual_message, f"Unexpected error message: {actual_message}"
