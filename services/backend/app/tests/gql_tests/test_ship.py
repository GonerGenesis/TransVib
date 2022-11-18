import pytest

async def test_create_ship(http_client):

    mutation = """
                mutation CreateShip {
                    createShip(ship: {title: "moep", description: "miep", authorId: 1}){
                    title
                    description
                    id
                    }
                } """
    payload = {"query": mutation}

    response = await http_client.post("/graphql", json=payload)
    json = response.json()
    print('test create ship', json)

    assert json["data"]["createShip"]["title"] == "moep"
    assert json["data"]["createShip"]["description"] == "miep"