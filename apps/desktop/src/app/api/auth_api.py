"""Authentication API endpoints."""

from app.api.client import ApiClient


class AuthApi:
    def __init__(self, client: ApiClient) -> None:
        self.client = client

    def register(self, email: str, password: str) -> dict:
        return self.client.post("/auth/register", {"email": email, "password": password})

    def login(self, email: str, password: str) -> dict:
        return self.client.post("/auth/login", {"email": email, "password": password})

    def get_me(self) -> dict:
        return self.client.get("/auth/me")
