import pytest

from app.db.models import FrameSegment, Frame
from tests.utils.utils import random_ship, random_frame, random_point, random_pos


def process_yaml(self, file):
    with open(file) as stream:
        try:
            args = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

        for i, point in enumerate(args['points']):
            if not point.get('id'):
                point['id'] = i + 1
        if 'lines' in args:
            args['segments'] = args.pop('lines')
        for i, segment in enumerate(args['segments']):
            if not segment.get('id'):
                segment['id'] = i + 1
            try:
                segment['start'] = segment.pop('from')
            except KeyError:
                pass
            try:
                segment['end'] = segment.pop('to')
            except KeyError:
                pass
            try:
                del segment['shared_edge']
            except KeyError:
                pass
        # print(args)
        if 'x' in args:
            args['frame_pos'] = args.pop('x')
    return args


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


async def test_create_frame(http_client):
    ship = await random_ship(1)
    pos = random_pos()
    mutation = """
                mutation CreateFrame {{
                    createFrame(frame: {{framePos: "{}", shipId: {}}}){{
                    framePos
                    id
                    }}
                }} """.format(pos, ship.id)
    payload = {"query": mutation}

    response = await http_client.post("/graphql", json=payload)
    json = response.json()
    print('test create frame', json)

    assert json["data"]["createFrame"]["id"] == (await Frame.all())[-1].id
    assert float(json["data"]["createFrame"]["framePos"]) == pytest.approx(pos, 1e-3)


# async def test_create_frame_with_geo(http_client):
#     ship = await random_ship(1)
#     mutation = """
#                     mutation CreateFrame {{
#                         createFrame(frame: {{framePos: "{}", shipId: {}}}){{
#                         framePos
#                         id
#                         }}
#                     }} """.format(pos, ship.id)
#     payload = {"query": mutation}
#
#     response = await http_client.post("/graphql", json=payload)
#     json = response.json()
#     print('test create frame with geo', json)
#
#     assert json["data"]["createFrame"]["id"] == (await Frame.all())[-1].id
#     assert float(json["data"]["createFrame"]["framePos"]) == pytest.approx(pos, 1e-3)


async def test_update_frame(http_client):
    frame = await random_frame(1)
    pos = random_pos()
    mutation = """
                mutation UpdateFrame {{
                    updateFrame(frameId: {} frame: {{framePos: {}}}){{
                    framePos
                    id
                    }}
                }} """.format(frame.id, pos)
    payload = {"query": mutation}

    response = await http_client.post("/graphql", json=payload)
    json = response.json()
    print('test update frame', json)

    assert json["data"]["updateFrame"]["id"] == frame.id
    assert float(json["data"]["updateFrame"]["framePos"]) == pytest.approx(pos, 1e-3)


async def test_delete_frame(http_client):
    frame = await random_frame(1)
    mutation = """
                mutation DeleteFrame {{
                    deleteFrame(id: {}){{
                        id
                        msg
                        type 
                    }}
                }}
            """.format(frame.id)
    payload = {"query": mutation}

    response = await http_client.post("/graphql", json=payload)
    json = response.json()
    print('test delete frame', json)

    assert json["data"]["deleteFrame"]["msg"] == "Deleted Frame {}".format(frame.id)
