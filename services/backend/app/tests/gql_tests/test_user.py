import pytest

from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from httpx import ASGITransport

from tortoise.contrib import test

#pytestmark = pytest.mark.asyncio


# async def test_empty_user(test_app_with_db)

@pytest.mark.asyncio
async def test_create_user(http_client):
    # transport = AIOHTTPTransport(url="http://0.0.0.0:5000/graphql")
    # client = Client(transport=transport, fetch_schema_from_transport=True)
    print(http_client.base_url)

    mutation = 'mutation CreateUser { createUser(user: {username: "geemo", fullName: "GK", password: "kaymo"}){username fullName}}'
    payload = {"query": mutation}

    response = await http_client.post("/graphql", json=payload)
    # test_request_payload = {"username": "geemo", "full_name": "GK", "password": "kaymo"}
    # test_response_payload = {"id": 1, "username": "gee", "full_name": "GK"}

    # async def mock_post(payload):
    #     return 1
    #
    # monkeypatch.setattr(users, "create_user", mock_post)
    json = response.json()
    print(json)

    assert json["data"]["createUser"]["username"] == "geemo"
