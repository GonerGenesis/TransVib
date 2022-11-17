import pytest

async def test_create_user(http_client):
    # transport = AIOHTTPTransport(url="http://0.0.0.0:5000/graphql")
    # client = Client(transport=transport, fetch_schema_from_transport=True)
    # print(http_client.base_url)

    mutation = 'mutation CreateShip { createShip(user: {username: "geemo", fullName: "GK", password: "kaymo"}){' \
               'username fullName}} '
    payload = {"query": mutation}

    response = await http_client.post("/graphql", json=payload)
    json = response.json()
    print('test create user', json)

    assert json["data"]["createUser"]["username"] == "geemo"