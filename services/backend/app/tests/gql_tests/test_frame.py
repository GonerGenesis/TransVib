import pytest

from app.db.models import FrameSegment
from tests.utils.utils import random_ship, random_frame, random_point


async def test_get_frame(http_client, random_setup):
    # ship = await random_ship(1)
    # frame = await random_frame(ship.id)
    # point_1 = await random_point(frame.id)
    # point_2 = await random_point(frame.id)
    # segment = await FrameSegment.create(frame_id=frame.id, start_point_id=point_1.id,
    #                                     end_point_id=point_2.id,
    #                                     thick=0.02)
    query = """
               query GetFrame {{
                   getFrame(id: {}) {{
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
                        ship{{
                            title
                        }}
                   }}
               }}
               """.format(random_setup['frame'].id)
    payload = {"query": query}
    response = await http_client.post("/graphql", json=payload)
    json = response.json()
    print('test get frame', json)

    assert json["data"]["getFrame"]["id"] == random_setup['frame'].id
    assert float(json["data"]["getFrame"]["framePos"]) == pytest.approx(float(random_setup['frame'].frame_pos))
    assert json["data"]["getFrame"]["ship"]["title"] == random_setup['ship'].title
    assert float(json["data"]["getFrame"]["framePoints"][0]["y"]) == pytest.approx(float(random_setup['p1'].y))
    assert float(json["data"]["getFrame"]["framePoints"][0]["z"]) == pytest.approx(float(random_setup['p1'].z))
    assert float(json["data"]["getFrame"]["framePoints"][1]["y"]) == pytest.approx(float(random_setup['p2'].y))
    assert float(json["data"]["getFrame"]["framePoints"][1]["z"]) == pytest.approx(float(random_setup['p2'].z))