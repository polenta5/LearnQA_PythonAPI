from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserDelete(BaseCase):
    #Ex18.1 - Попытка удалить пользователя по ID 2
    def test_negative_delete_user_2(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response_1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response_1, 'auth_sid')
        token = self.get_header(response_1, 'x-csrf-token')

        response_2 = MyRequests.delete(
            f"/user/2",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        Assertions.assert_code_status(response_2, 400)
        expected_message = f"Please, do not delete test users with ID 1, 2, 3, 4 or 5."
        actual_message = response_2.content.decode("utf-8")
        assert expected_message in actual_message, f"Unexpected error message: {actual_message}"

    #Ex18.2 - Позитивный тест на удаление
    def test_delete_user(self):
        data = self.prepare_registration_data()
        response_1 = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response_1, 200)
        Assertions.assert_json_has_key(response_1, "id")

        email = data['email']
        password = data['password']
        user_id = self.get_json_value(response_1, "id")

        response_2 = MyRequests.post("/user/login", data={
            "email": email,
            "password": password
        })

        auth_sid = self.get_cookie(response_2, 'auth_sid')
        token = self.get_header(response_2, 'x-csrf-token')

        response_3 = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        Assertions.assert_code_status(response_3, 200)


    #Ex18.3 - Негативный, попробовать удалить пользователя, будучи авторизованными другим пользователем
    def test_negative_delete_user_with_auth_other_user(self):
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
        user_id_2 = self.get_json_value(response_2, "id")

        response_3 = MyRequests.delete(
            f"/user/{user_id_2}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_code_status(response_3, 400)
        expected_message = f"This user can only delete their own account."
        actual_message = response_3.content.decode("utf-8")
        assert expected_message in actual_message, f"Unexpected error message: {actual_message}"