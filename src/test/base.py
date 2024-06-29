from fastapi import FastAPI
from httpx import AsyncClient


class Client:
    def __init__(self, app: FastAPI):
        self.client = AsyncClient(app=app, base_url="http://127.0.0.1/")

    async def get(self, path: str, token: str | None = None):
        headers = {}
        if token is not None:
            headers["Authorization"] = f"Bearer {token}"
        result = await self.client.get(path, headers=headers)
        return result

    async def post(self, path: str, json_data, token: str | None = None):
        headers = {}
        if token is not None:
            headers["Authorization"] = f"Bearer {token}"
        result = await self.client.post(path, json=json_data, headers=headers)
        return result

    async def put(self, path: str, json_data: dict, token: str | None = None):
        headers = {}
        if token is not None:
            headers["Authorization"] = f"Bearer {token}"
        result = await self.client.put(path, json=json_data, headers=headers)
        return result

    async def delete(self, path: str, token: str | None = None):
        headers = {}
        if token is not None:
            headers["Authorization"] = f"Bearer {token}"
        result = await self.client.delete(path, headers=headers)
        return result
