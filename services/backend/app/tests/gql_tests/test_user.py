import pytest

from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from httpx import ASGITransport

from tortoise.contrib import test

#pytestmark = pytest.mark.asyncio


async def test_empty_user(http_client):
    mutation = 'mutation CreateUser { createUser(user: {username: "", fullName: "", password: ""}){username fullName}}'
    payload = {"query": mutation}

    response = await http_client.post("/graphql", json=payload)
    print(response.status_code)
    json = response.json()
    print('test empty user', json)

    assert json["errors"] is not None


async def test_create_user(http_client):
    # transport = AIOHTTPTransport(url="http://0.0.0.0:5000/graphql")
    # client = Client(transport=transport, fetch_schema_from_transport=True)
    print(http_client.base_url)

    mutation = 'mutation CreateUser { createUser(user: {username: "geemo", fullName: "GK", password: "kaymo"}){' \
               'username fullName}} '
    payload = {"query": mutation}

    response = await http_client.post("/graphql", json=payload)
    json = response.json()
    print('test create user', json)

    assert json["data"]["createUser"]["username"] == "geemo"


async def test_get_user(http_client):
    query = """
    query GetUser {
        getUser(id: 1) {
            id
            username
        }
    }
    """
    payload = {"query": query}
    response = await http_client.post("/graphql", json=payload)
    json = response.json()
    print('test create user', json)

    assert json["data"]["getUser"]["username"] == "admin@gschwifast.com"
    assert json["data"]["getUser"]["id"] == 1



async def test_update_user(http_client):
    mutation = """
        mutation UpdateUser {
            updateUser(user: {userId: 1, fullName: "knickerbocker"}){ 
               fullName
            }
        }
    """
    payload = {"query": mutation}

    response = await http_client.post("/graphql", json=payload)
    json = response.json()
    print('test create user', json)

    assert json["data"]["updateUser"]["full_name"] == "knickerbocker"