import pytest
from fastapi import status

from api.app import app
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient


class TestHeroEndpoints:
    _test_client = TestClient(app)
    _response_mocks = {
        "Batman": {
            "response": "success",
            "results": [
                {
                    "id": "1",
                    "name": "Batman",
                    "powerstats": {
                        "intelligence": "100",
                        "strength": "100",
                        "speed": "100",
                        "power": "100"
                    }
                }
            ]
        },
        "Hulk": {
            "response": "success",
            "results": [
                {
                    "id": "2",
                    "name": "Hulk",
                    "powerstats": {
                        "intelligence": "50",
                        "strength": "50",
                        "speed": "50",
                        "power": "50"
                    }
                }
            ]
        },
        "Thor": {
            "response": "success",
            "results": [
                {
                    "id": "3",
                    "name": "Thor",
                    "powerstats": {
                        "intelligence": "75",
                        "strength": "75",
                        "speed": "75",
                        "power": "75"
                    }
                }
            ]
        },
        "Iron Man": {
            "response": "success",
            "results": [
                {
                    "id": "4",
                    "name": "Iron Man",
                    "powerstats": {
                        "intelligence": "25",
                        "strength": "25",
                        "speed": "25",
                        "power": "25"
                    }
                }
            ]
        }
    }

    async def _create_heroes_in_db(self, search_mock: AsyncMock):
        for hero_name in self._response_mocks.keys():
            search_mock.return_value = self._response_mocks[hero_name]
            self._test_client.post("/hero/", json={"name": hero_name})

    @patch("handlers.hero_handler.HttpClient.search_hero")
    @pytest.mark.asyncio
    async def test_search_and_create_hero_success(self, search_mock: AsyncMock):
        search_mock.return_value = self._response_mocks["Batman"]
        response = self._test_client.post("/hero/", json={"name": "Batman"})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == {
            "status": "success",
            "results": [
                {
                    "id": 1,
                    "name": "Batman",
                    "intelligence": 100,
                    "strength": 100,
                    "speed": 100,
                    "power": 100
                }
            ]}

    @patch("handlers.hero_handler.HttpClient.search_hero")
    @pytest.mark.asyncio
    async def test_search_and_create_hero_not_found(self, search_mock: AsyncMock):
        search_mock.return_value = {"response": "error", "error": "character with given name not found"}
        response = self._test_client.post("/hero/", json={"name": "Not Batman"})

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "Character with given name not found"}

    @patch("handlers.hero_handler.HttpClient.search_hero")
    @pytest.mark.asyncio
    async def test_search_and_create_hero_conflict(self, search_mock: AsyncMock):
        search_mock.return_value = self._response_mocks["Hulk"]
        response = self._test_client.post("/hero/", json={"name": "Hulk"})

        assert response.status_code == status.HTTP_201_CREATED

        response = self._test_client.post("/hero/", json={"name": "Hulk"})

        assert response.status_code == status.HTTP_409_CONFLICT
        assert response.json() == {"detail": "Heroes already exist in the database."}

    @patch("handlers.hero_handler.HttpClient.search_hero")
    @pytest.mark.asyncio
    async def test_get_heroes_all(self, search_mock: AsyncMock):
        await self._create_heroes_in_db(search_mock)

        response = self._test_client.get("/hero/")
        
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == [
            {
                "id": 1,
                "name": "Batman",
                "intelligence": 100,
                "strength": 100,
                "speed": 100,
                "power": 100
            },
            {
                "id": 2,
                "name": "Hulk",
                "intelligence": 50,
                "strength": 50,
                "speed": 50,
                "power": 50
            },
            {
                "id": 3,
                "name": "Thor",
                "intelligence": 75,
                "strength": 75,
                "speed": 75,
                "power": 75
            },
            {
                "id": 4,
                "name": "Iron Man",
                "intelligence": 25,
                "strength": 25,
                "speed": 25,
                "power": 25
            }
    ]

    @patch("handlers.hero_handler.HttpClient.search_hero")
    @pytest.mark.asyncio
    async def test_get_heroes_filtered(self, search_mock: AsyncMock):
        await self._create_heroes_in_db(search_mock)

        response_batman = self._test_client.get("/hero/?name=Batman")
        response_hulk = self._test_client.get("/hero/?name=Hulk")
        response_not_found = self._test_client.get("/hero/?name=Hulks")
        response_intelligence = self._test_client.get("/hero/?intelligence=25")
        response_strength_gte = self._test_client.get("/hero/?strength__gte=50")
        response_power_lte = self._test_client.get("/hero/?power__lte=50")

        assert response_batman.status_code == status.HTTP_200_OK
        assert response_batman.json() == [
            {
                "id": 1,
                "name": "Batman",
                "intelligence": 100,
                "strength": 100,
                "speed": 100,
                "power": 100
            }
        ]

        assert response_hulk.status_code == status.HTTP_200_OK
        assert response_hulk.json() == [
            {
                "id": 2,
                "name": "Hulk",
                "intelligence": 50,
                "strength": 50,
                "speed": 50,
                "power": 50
            }
        ]
        
        assert response_not_found.status_code == status.HTTP_404_NOT_FOUND
        assert response_not_found.json() == {"message": "No heroes found."}

        assert response_intelligence.status_code == status.HTTP_200_OK
        assert response_intelligence.json() == [
            {
                "id": 4,
                "name": "Iron Man",
                "intelligence": 25,
                "strength": 25,
                "speed": 25,
                "power": 25
            }
        ]

        assert response_strength_gte.status_code == status.HTTP_200_OK
        assert response_strength_gte.json() == [
            {
                "id": 1,
                "name": "Batman",
                "intelligence": 100,
                "strength": 100,
                "speed": 100,
                "power": 100
            },
            {
                "id": 2,
                "name": "Hulk",
                "intelligence": 50,
                "strength": 50,
                "speed": 50,
                "power": 50
            },
            {
                "id": 3,
                "name": "Thor",
                "intelligence": 75,
                "strength": 75,
                "speed": 75,
                "power": 75
            }
        ]

        assert response_power_lte.status_code == status.HTTP_200_OK
        assert response_power_lte.json() == [
            {
                "id": 2,
                "name": "Hulk",
                "intelligence": 50,
                "strength": 50,
                "speed": 50,
                "power": 50
            },
            {
                "id": 4,
                "name": "Iron Man",
                "intelligence": 25,
                "strength": 25,
                "speed": 25,
                "power": 25
            }
        ]
