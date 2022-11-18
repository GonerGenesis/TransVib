import pytest

from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from httpx import ASGITransport

from tortoise.contrib import test

from tests.utils.utils import random_ship


# pytestmark = pytest.mark.asyncio


async def test_empty_user(http_client):
    mutation = 'mutation CreateUser { createUser(user: {username: " ", fullName: "", password: ""}){username fullName}}'
    payload = {"query": mutation}

    response = await http_client.post("/graphql", json=payload)
    print(response.status_code)
    json = response.json()
    print('test empty user', json)

    assert json["errors"] is not None
    assert "empty" in json["errors"][0]['message']


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
    ship = await random_ship(1)
    query = """
    query GetUser {
        getUser(id: 1) {
            id
            username
            ships{
                title
                id
            }
        }
    }
    """
    payload = {"query": query}
    response = await http_client.post("/graphql", json=payload)
    json = response.json()
    print('test get user', json)

    assert json["data"]["getUser"]["username"] == "admin@gschwifast.com"
    assert json["data"]["getUser"]["id"] == 1
    assert json["data"]["getUser"]["ships"][-1]["id"] == ship.id
    assert json["data"]["getUser"]["ships"][-1]["title"] == ship.title



async def test_update_user(http_client):
    mutation = """
        mutation UpdateUser {
            updateUser(userId: 1, user: {fullName: "knickerbocker"}){ 
               fullName
            }
        }
    """
    payload = {"query": mutation}

    response = await http_client.post("/graphql", json=payload)
    json = response.json()
    print('test update user', json)

    assert json["data"]["updateUser"]["fullName"] == "knickerbocker"


async def test_delete_user(http_client):
    mutation = """
            mutation DeleteUser {
                deleteUser(id: 2){
                    id
                    msg
                    type 
                }
            }
        """
    payload = {"query": mutation}

    response = await http_client.post("/graphql", json=payload)
    json = response.json()
    print('test delete user', json)

    assert json["data"]["deleteUser"]["msg"] == "Deleted User 2"
