import pytest

from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

pytestmark = pytest.mark.asyncio


async def test_create_user(test_app_with_db):
    transport = AIOHTTPTransport(url="http://0.0.0.0:5000/graphql")
    client = Client(transport=transport, fetch_schema_from_transport=True)

    query = gql(
        """
        mutation CreateUser {
            createUser(user: {username: "geemo", fullName: "GK", password: "kaymo"}){
            username
            fullName
            }
        }
        """
    )
    # test_request_payload = {"username": "geemo", "full_name": "GK", "password": "kaymo"}
    # test_response_payload = {"id": 1, "username": "gee", "full_name": "GK"}

    # async def mock_post(payload):
    #     return 1
    #
    # monkeypatch.setattr(users, "create_user", mock_post)

    response = await client.execute_async(query)
    print(response)

    assert response["user"]["username"] == "geemo"
