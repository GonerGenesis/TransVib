import decimal

import pytest

from app.db.models import FramePoint, Frame, FrameSegment
from app.db.schemas import FrameSchema
from tests.utils.utils import random_point


async def test_get_point(http_client, create_test_frame):
    point_1 = await random_point(create_test_frame.id)
    point_2 = await random_point(create_test_frame.id)
    segment = await FrameSegment.create(frame_id=create_test_frame.id, start_point_id=point_1.id, end_point_id=point_2.id,
                                 thick=0.02)
    query = """
       query GetPoint {{
           getPoint(id: {}) {{
               id
               y
               z
               startsSegments{{
                id
               }}
           }}
       }}
       """.format(point_1.id)
    payload = {"query": query}
    response = await http_client.post("/graphql", json=payload)
    json = response.json()
    print('test get point', json)

    assert json["data"]["getPoint"]["id"] == point_1.id
    assert float(json["data"]["getPoint"]["y"]) == pytest.approx(float(point_1.y))
    assert float(json["data"]["getPoint"]["z"]) == pytest.approx(float(point_1.z))
    assert json["data"]["getPoint"]["startsSegments"][0]["id"] == segment.id


async def test_create_point(http_client, create_test_frame):
    frame_id = create_test_frame.id
    mutation = """
        mutation CreatePoint{
            createPoint(point: {y: "6.0", z: "5.0", frameId: %s}){
                id
                y
                z
                frame{
                        id
                    }
            }
        }
    """ % frame_id
    payload = {"query": mutation}

    response = await http_client.post("/graphql", json=payload)
    json = response.json()
    frame = await FrameSchema.from_queryset(Frame.all())
    print('test frame is', frame)
    print('test create point', json)

    assert json["data"]["createPoint"]["frame"]["id"] == frame_id
    assert float(json["data"]["createPoint"]["y"]) == pytest.approx(6)
    assert float(json["data"]["createPoint"]["z"]) == pytest.approx(5)


async def test_update_point(http_client, create_test_frame):
    point: FramePoint = await random_point(create_test_frame.id)
    mutation = """
           mutation UpdatePoint{
               updatePoint(point: {y: "12.0", z: "14.0"}, pointId: %s){
                   id
                   y
                   z
                   frame{
                        id
                    }
               }
           }
       """ % point.id

    payload = {"query": mutation}

    response = await http_client.post("/graphql", json=payload)
    json = response.json()
    print('test update point', json)

    assert json["data"]["updatePoint"]["id"] == point.id
    assert json["data"]["updatePoint"]["frame"]["id"] == create_test_frame.id
    assert float(json["data"]["updatePoint"]["y"]) == pytest.approx(12)
    assert float(json["data"]["updatePoint"]["z"]) == pytest.approx(14)


async def test_delete_point(http_client, create_test_frame):
    point = await random_point(create_test_frame.id)
    mutation = """
                mutation DeletePoint {{
                    deletePoint(id: {}){{
                        id
                        msg
                        type 
                    }}
                }}
            """.format(point.id)
    payload = {"query": mutation}

    response = await http_client.post("/graphql", json=payload)
    json = response.json()
    print('test delete point', json)

    assert json["data"]["deletePoint"]["msg"] == "Deleted FramePoint {}".format(point.id)
