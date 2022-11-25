import pytest

async def test_get_frame(http_client, no_random_setup):
    query = """
               query GetFrameCSValues {{
                   getCsValues(id: {}) {{
                        frameId
                        center{{
                        y
                        z
                        }}
                   }}
               }}
               """.format(no_random_setup['frame'].id)
    payload = {"query": query}
    response = await http_client.post("/graphql", json=payload)
    json = response.json()
    print('test get cs values', json)

    assert json["data"]["getCsValues"]["frameId"] == no_random_setup['frame'].id
    assert json["data"]["getCsValues"]["center"] == {'y': 1.0, 'z': 2.0}
    # assert float(json["data"]["getCsValues"]["center"]) == pytest.approx(float(random_setup['frame'].frame_pos))
