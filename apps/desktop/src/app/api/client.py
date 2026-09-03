"""HTTP API Client connecting to FastAPI backend."""

import httpx
from typing import Any


class ApiClient:
    def __init__(self, base_url: str = "http://localhost:8000/api/v1") -> None:
        self.base_url = base_url.rstrip("/")
        self.token: str | None = None

    def set_token(self, token: str | None) -> None:
        self.token = token

    def _headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def get(self, endpoint: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        with httpx.Client(timeout=10.0) as client:
            res = client.get(url, headers=self._headers(), params=params)
            res.raise_for_status()
            return res.json()

    def post(self, endpoint: str, json_data: dict[str, Any]) -> dict[str, Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        with httpx.Client(timeout=10.0) as client:
            res = client.post(url, headers=self._headers(), json=json_data)
            res.raise_for_status()
            return res.json()

    def put(self, endpoint: str, json_data: dict[str, Any]) -> dict[str, Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        with httpx.Client(timeout=10.0) as client:
            res = client.put(url, headers=self._headers(), json=json_data)
            res.raise_for_status()
            return res.json()

    def delete(self, endpoint: str) -> None:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        with httpx.Client(timeout=10.0) as client:
            res = client.delete(url, headers=self._headers())
            res.raise_for_status()
