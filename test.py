import random
import time

import requests

BASE_URL = "http://localhost:8080/api/v1"


def get_jwt():
    resp = requests.post(f"{BASE_URL}/auth")
    resp.raise_for_status()
    jwt_token = resp.json()["jwt_token"]
    return jwt_token


def start_test(jwt_token):
    headers = {"Authorization": f"Bearer {jwt_token}"}
    resp = requests.post(f"{BASE_URL}/test/start", json={"test_id": TEST_ID}, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    return data["result_id"]


def get_questions_list(jwt_token, test_id):
    headers = {"Authorization": f"Bearer {jwt_token}"}
    resp = requests.get(f"{BASE_URL}/question/list?test_id={test_id}", headers=headers)
    resp.raise_for_status()
    return resp.json()["questions_id"]


def submit_answer(jwt_token, question_id, result_id):
    headers = {"Authorization": f"Bearer {jwt_token}"}
    # Случайный вариант ответа (1, 2 или 3)
    variant_id = random.randint(1, 3)
    resp = requests.post(
        f"{BASE_URL}/answer/submit",
        json={"question_id": question_id, "variant_id": variant_id, "result_id": result_id},
        headers=headers
    )
    resp.raise_for_status()


def finish_test(jwt_token, result_id):
    headers = {"Authorization": f"Bearer {jwt_token}"}
    resp = requests.post(f"{BASE_URL}/test/finish", json={"result_id": result_id}, headers=headers)
    resp.raise_for_status()
    return resp.json()


TEST_ID = 2

print("Получаем JWT...")
jwt = get_jwt()
print("JWT:", jwt)

print("Запускаем тест...")
RESULT_ID = start_test(jwt)
print("result_id:" + str(RESULT_ID))

questions = get_questions_list(jwt_token=jwt, test_id=TEST_ID)

# print(questions)
#
print("Отвечаем на вопросы...")
for question_id in questions:
    print(f"Вопрос {question_id}: отвечаем случайно...")
    submit_answer(jwt, question_id, RESULT_ID)
    time.sleep(1.1)  # чтобы не спамить API

print("Завершаем тест...")
test_result = finish_test(jwt_token=jwt, result_id=RESULT_ID)
print(test_result)
