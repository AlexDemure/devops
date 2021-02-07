import random
import string
from locust import HttpUser, task, between


class TestAccountData:

    email = None
    hashed_password = "string"
    city = "Челябинск"

    def __init__(self):
        self.email = f"{self.generate_random_code(only_digits=False)}@gmail.com"

    def get_personal_data(self) -> dict:
        return dict(
            email=self.email,
            hashed_password=self.hashed_password,
            city=self.city
        )

    @staticmethod
    def generate_random_code(size=6, only_digits: bool = True):
        if only_digits:
            chars = string.digits
        else:
            chars = string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for _ in range(size))


class QuickstartUser(HttpUser):
    wait_time = between(1, 2.5)

    @task
    def registration(self):
        account_data = TestAccountData()

        response = self.client.post("/api/v1/accounts/", json=account_data.get_personal_data())
        assert response.status_code == 201
        headers = {"Authorization": f"Bearer {response.json()['access_token']}"}

        response = self.client.post("/api/v1/accounts/confirm/", headers=headers, json={"code": "123456"})
        assert response.status_code == 200
