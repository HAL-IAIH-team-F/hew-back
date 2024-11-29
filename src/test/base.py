import json
from dataclasses import asdict, is_dataclass
from typing import Any

import pydantic
from fastapi import FastAPI
from httpx import AsyncClient
from pydantic import BaseModel, TypeAdapter
from pydantic.dataclasses import is_pydantic_dataclass


class Client:
    def __init__(self, app: FastAPI):
        self.client = AsyncClient(app=app, base_url="http://127.0.0.1/")

    async def get(self, path: str, token: str | None = None):
        headers = {}
        if token is not None:
            headers["Authorization"] = f"Bearer {token}"
        result = await self.client.get(path, headers=headers)
        return result

    async def post(self, path: str, json_data: pydantic.BaseModel | Any, token: str | None = None):
        headers = {}
        if token is not None:
            headers["Authorization"] = f"Bearer {token}"
        if isinstance(json_data, BaseModel):
            result = await self.client.post(path, content=json_data.model_dump_json(), headers=headers)
        elif is_pydantic_dataclass(type(json_data)):
            print(f"base.pyより--->{json_data}")
            result = await self.client.post(path, content=TypeAdapter(type(json_data)).dump_json(json_data), headers=headers)
        else:
            print(f"base.pyより--->{json_data}")
            raise ValueError

        return result

    async def put(self, path: str, json_data: pydantic.BaseModel, token: str | None = None):
        headers = {}
        if token is not None:
            headers["Authorization"] = f"Bearer {token}"
        result = await self.client.put(path, content=json_data.model_dump_json(), headers=headers)
        return result

    async def delete(self, path: str, token: str | None = None):
        headers = {}
        if token is not None:
            headers["Authorization"] = f"Bearer {token}"
        result = await self.client.delete(path, headers=headers)
        return result
