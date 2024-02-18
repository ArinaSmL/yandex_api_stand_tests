import sender_stand_request
import data

user_body = {
    "firstName": "Tолий",
    "phone": "+79995553322",
    "address": "г. Москва, ул. Пушкина, д. 10"
}

def get_user_body(first_name):
    current_body = data.user_body.copy()
    current_body["firstName"] = first_name
    return current_body


def test_create_user_2_letter_in_first_name_get_success_response():
    user_body = get_user_body("Tол")
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 201
    assert user_response.json()["authToken"] != ''
    users_table_response = sender_stand_request.get_users_table()
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
           + user_body["address"] + ",,," + user_response.json()["authToken"]
    assert users_table_response.text.count(str_user) == 1

def positive_assert(first_name):
    user_body = get_user_body(first_name)
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 201
    assert user_response.json()["authToken"] != ""
    users_table_response = sender_stand_request.get_users_table()
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]
    assert users_table_response.text.count(str_user) == 1


def test_create_user_2_letter_in_first_name_get_success_response(): #1
    positive_assert("Aa")

def test_create_user_2_letter_in_first_name_get_success_response(): #2
    positive_assert("AaаааAaаааAaааа")

def negative_assert_symbol(first_name):
    user_body = get_user_body(first_name)
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 400 , "Екгу"
    assert user_response.json()["code"] == 400 , 'OK'
    assert user_response.json()["message"] == "Имя пользователя введено некорректно. " \
                                         "Имя может содержать только русские или латинские буквы, " \
                                         "длина должна быть не менее 2 и не более 15 символов"

def test_create_user_16_letter_in_first_name_get_error_response(): #3
    negative_assert_symbol('A')

def test_create_user_16_letter_in_first_name_get_error_response(): #4
    negative_assert_symbol("AaаааAaаааAaаааа")

def test_create_user_english_letter_in_first_name_get_success_response(): #5
    positive_assert("Fantik")

def test_create_user_russian_letter_in_first_name_get_success_response(): #6
    positive_assert("Мария")

def test_create_user_has_space_in_first_name_get_error_response(): #7
    negative_assert_symbol(' Van')

def test_create_user_has_special_symbol_in_first_name_get_error_response(): #8
    negative_assert_symbol('T&J')

def test_create_user_has_number_in_first_name_get_error_response(): #9
    negative_assert_symbol('Tom0')

def negative_assert_no_first_name(user_body):
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert response.json()["message"] == "Не все необходимые параметры были переданы"

def test_create_user_no_first_name_get_error_response(): #10
    user_body = data.user_body.copy()
    user_body.pop("firstName")
    negative_assert_no_first_name(user_body)

def test_create_user_empty_first_name_get_error_response(): #11
    user_body = get_user_body("")
    negative_assert_no_first_name(user_body)

def test_create_user_number_type_first_name_get_error_response(): #12
    user_body = get_user_body(12)
    response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 400