import pytest

from app.db.models import FrameSegment
from tests.utils.utils import random_ship, random_frame, random_point


async def test_get_ship(http_client):
    ship = await random_ship(1)
    frame = await random_frame(ship.id)
    point_1 = await random_point(frame.id)
    point_2 = await random_point(frame.id)
    segment = await FrameSegment.create(frame_id=frame.id, start_point_id=point_1.id,
                                        end_point_id=point_2.id,
                                        thick=0.02)
    query = """
           query GetShip {{
               getShip(id: {}) {{
                   id
                   title
                   description
                   author{{
                    id
                    username
                   }}
                   frames{{
                    id
                    framePos
                    frameSegments{{
                        id
                        thick
                    }}
                    framePoints{{
                        id
                        y
                        z
                    }}
                   }}
               }}
           }}
           """.format(ship.id)
    payload = {"query": query}
    response = await http_client.post("/graphql", json=payload)
    json = response.json()
    print('test get ship', json)

    assert json["data"]["getShip"]["id"] == ship.id
    assert json["data"]["getShip"]["title"] == ship.title
    assert json["data"]["getShip"]["description"] == ship.description
    assert json["data"]["getShip"]["author"]["id"] == 1
    assert float(json["data"]["getShip"]["frames"][0]["framePoints"][0]["y"]) == pytest.approx(float(point_1.y))
    assert float(json["data"]["getShip"]["frames"][0]["framePoints"][0]["z"]) == pytest.approx(float(point_1.z))
    assert float(json["data"]["getShip"]["frames"][0]["framePoints"][1]["y"]) == pytest.approx(float(point_2.y))
    assert float(json["data"]["getShip"]["frames"][0]["framePoints"][1]["z"]) == pytest.approx(float(point_2.z))
    assert json["data"]["getShip"]["frames"][0]["frameSegments"][0]["id"] == segment.id
    assert float(json["data"]["getShip"]["frames"][0]["frameSegments"][0]["thick"]) == pytest.approx(
        float(segment.thick))
    assert json["data"]["getShip"]["frames"][0]["id"] == frame.id
    assert float(json["data"]["getShip"]["frames"][0]["framePos"]) == pytest.approx(float(frame.frame_pos))


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


async def test_update_ship(http_client):
    ship = await random_ship(1)
    mutation = """
                mutation UpdateShip {{
                    updateShip(shipId: {} ship: {{title: "blub", description: "blab"}}){{
                    title
                    description
                    id
                    }}
                }} """.format(ship.id)
    payload = {"query": mutation}

    response = await http_client.post("/graphql", json=payload)
    json = response.json()
    print('test update ship', json)

    assert json["data"]["updateShip"]["title"] == "blub"
    assert json["data"]["updateShip"]["description"] == "blab"


async def test_delete_ship(http_client):
    ship = await random_ship(1)
    mutation = """
                mutation DeleteShip {{
                    deleteShip(id: {}){{
                        id
                        msg
                        type 
                    }}
                }}
            """.format(ship.id)
    payload = {"query": mutation}

    response = await http_client.post("/graphql", json=payload)
    json = response.json()
    print('test delete ship', json)

    assert json["data"]["deleteShip"]["msg"] == "Deleted Ship {}".format(ship.id)
