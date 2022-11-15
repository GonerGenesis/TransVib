import pytest

async def test_create_point(http_client):
    mutation = 'mutation CreatePoint { createPoint(point: {y: "", fullName: "GK", password: "kaymo"}){' \
               'username fullName}} '
    payload = {"query": mutation}

    response = await http_client.post("/graphql", json=payload)
    json = response.json()
    print('test create point', json)

    assert json["data"]["createUser"]["username"] == "geemo"

