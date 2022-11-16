import decimal

import pytest

from app.db.models import FramePoint, Frame
from app.db.schemas import FrameSchema
from tests.utils.utils import random_point


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
               createPoint(point: {y: "12.0", z: "14.0", frameId: %s}){
                   id
                   y
                   z
                   frame{
                        id
                    }
               }
           }
       """ % create_test_frame.id

    payload = {"query": mutation}

    response = await http_client.post("/graphql", json=payload)
    json = response.json()
    print('test update point', json)

    assert json["data"]["updatePoint"]["id"] == point.id
    assert json["data"]["updatePoint"]["frame"]["id"] == point.id
    assert float(json["data"]["updatePoint"]["y"]) == pytest.approx(6)
    assert float(json["data"]["updatePoint"]["z"]) == pytest.approx(5)
