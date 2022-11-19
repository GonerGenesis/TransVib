import decimal

import pytest

from app.db.models import FrameSegment
from app.db.schemas import FrameSchema, FrameSegmentSchema
from tests.utils.utils import random_frame, random_pos, random_segment, random_point


async def test_get_segment(http_client, random_setup):
    query = """
       query GetSegment {{
           getSegment(id: {}) {{
               id
               thick               
               startPoint{{
                id
                y
                z
               }}
               endPoint{{
                id
                y
                z
               }}
               frame{{
                id
                framePos
               }}
           }}
       }}
       """.format(random_setup["segment"].id)
    payload = {"query": query}
    response = await http_client.post("/graphql", json=payload)
    json = response.json()
    print('test get frame segment', json)

    assert json["data"]["getSegment"]["id"] == random_setup['segment'].id
    assert float(json["data"]["getSegment"]["thick"]) == pytest.approx(float(random_setup['segment'].thick))
    assert float(json["data"]["getSegment"]["startPoint"]['y']) == pytest.approx(float(random_setup['p1'].y))
    assert float(json["data"]["getSegment"]["startPoint"]['z']) == pytest.approx(float(random_setup['p1'].z))
    assert json["data"]["getSegment"]["startPoint"]['id'] == pytest.approx(float(random_setup['p1'].id))
    assert float(json["data"]["getSegment"]["endPoint"]['y']) == pytest.approx(float(random_setup['p2'].y))
    assert float(json["data"]["getSegment"]["endPoint"]['z']) == pytest.approx(float(random_setup['p2'].z))
    assert json["data"]["getSegment"]["endPoint"]['id'] == random_setup['p2'].id
    assert json["data"]["getSegment"]["frame"]['id'] == random_setup['frame'].id
    assert float(json["data"]["getSegment"]["frame"]['framePos']) == pytest.approx(float(random_setup['frame'].frame_pos))


async def test_create_segment(http_client, random_setup):
    thick = random_pos()
    p1 = await random_point(random_setup['frame'].id)
    p2 = await random_point(random_setup['frame'].id)
    mutation = """
        mutation CreateSegment{{
            createSegment(segment: {{thick: "{}", endPointId: {}, startPointId: {}, frameId: {}}}){{
                id
                thick
                startPoint{{id}}
                endPoint{{id}}
                frame{{
                        id
                    }}
            }}
        }}
    """.format(thick, p2.id, p1.id, random_setup['frame'].id)
    payload = {"query": mutation}

    response = await http_client.post("/graphql", json=payload)
    json = response.json()
    segment = (await FrameSegmentSchema.from_queryset(FrameSegment.all()))[-1]
    # print('test segment is', segment)
    print('test create segment', json)

    assert json["data"]["createSegment"]["frame"]["id"] == random_setup['frame'].id
    assert json["data"]["createSegment"]["startPoint"]["id"] == p1.id
    assert json["data"]["createSegment"]["endPoint"]["id"] == p2.id
    assert json["data"]["createSegment"]["id"] == segment.id
    assert float(json["data"]["createSegment"]["thick"]) == pytest.approx(thick)


async def test_update_segment(http_client, random_setup):
    thick = random_pos()
    print(random_setup['segment'].thick)
    mutation = """
           mutation UpdateSegment{{
               updateSegment(segmentId: {}, segment: {{thick: {}}}){{
                   id
                   thick
                   frame{{
                        id
                    }}
               }}
           }}
       """.format(random_setup["segment"].id, thick)

    payload = {"query": mutation}

    response = await http_client.post("/graphql", json=payload)
    json = response.json()
    print('test update segment', json)
    segment = await FrameSegment.get(id=random_setup['segment'].id)
    print(segment.__dict__)

    assert json["data"]["updateSegment"]["id"] == random_setup["segment"].id
    assert json["data"]["updateSegment"]["frame"]["id"] == random_setup["frame"].id
    assert float(json["data"]["updateSegment"]["thick"]) == pytest.approx(float(segment.thick))


async def test_delete_point(http_client, random_setup):
    segment = await random_segment(random_setup['frame'].id)
    print(segment.__dict__)
    mutation = """
                mutation DeleteSegment {{
                    deleteSegment(id: {}){{
                        id
                        msg
                        type 
                    }}
                }}
            """.format(segment.id)
    payload = {"query": mutation}

    response = await http_client.post("/graphql", json=payload)
    json = response.json()
    print('test delete segment', json)

    assert json["data"]["deleteSegment"]["msg"] == "Deleted FrameSegment {}".format(segment.id)
