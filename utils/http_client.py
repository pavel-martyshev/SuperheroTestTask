from typing import Any

import aiohttp
from aiohttp import ClientResponseError

from config import Config, get_config


class HttpClient:
    _config: Config = get_config()

    @staticmethod
    async def _request_executor(url: str, method: str = "GET", **kwargs) -> dict[str, Any]:
        async with aiohttp.ClientSession() as session:
            async with session.request(method.upper(), url, **kwargs) as response:
                if response.status != 200:
                    raise ClientResponseError(history=response.history, request_info=response.request_info)

                result = await response.json()

                return result

    @classmethod
    async def search_hero(cls, hero_name: str):
        try:
            return await cls._request_executor(cls._config.search_url + f"/{hero_name}")
        except ClientResponseError:
            return None
        except Exception as e:
            raise e
