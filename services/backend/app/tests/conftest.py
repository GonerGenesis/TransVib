import asyncio
import os

import pytest
import nest_asyncio

from starlette.testclient import TestClient
from httpx import AsyncClient, ASGITransport

from gql import Client
from tortoise.contrib.test import finalizer, initializer
from tortoise import connections, Tortoise

from typing import Dict

from app.core.config import get_settings, Settings
from app.db.functions.initialise import TORTOISE_ORM
from app.main import create_application
from app.db.models import Ship, Frame, FramePoint, FrameSegment, FrameCSValues
from app.db.schemas import UserSchemaCreate
from app.db import functions

from tests.utils.utils import get_superuser_token_headers, random_pos, random_ship, random_frame

nest_asyncio.apply()


def get_settings_override():
    return Settings(testing=1, database_url=os.environ.get("DATABASE_TEST_URL"))


@pytest.fixture(scope="session")
async def test_app():
    # set up
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override

    # tear down


@pytest.fixture(scope="session", autouse=True)
@pytest.mark.asyncio
async def test_app_with_db(request, event_loop):
    # set up
    print(event_loop)
    print("blub")
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override
    db_url = os.environ.get("DATABASE_TEST_URL")
    initializer(["app.db.models.models"], db_url=db_url, app_label="models", loop=event_loop)
    request.addfinalizer(finalizer)
    yield app


@pytest.fixture(scope="session")
async def http_client(test_app_with_db):
    async with AsyncClient(app=test_app_with_db, base_url="http://test") as test_client:
        print(await test_client.get(url="/"))
        # print(test_client.base_url)
        yield test_client


@pytest.fixture(scope="session", autouse=True)
# @pytest.mark.asyncio
async def set_initial_data(test_app_with_db):
    db_url = os.environ.get("DATABASE_TEST_URL")
    # new_loop = asyncio.new_event_loop()
    print(db_url)
    await Tortoise.init(db_url=db_url, modules={"models": ["app.db.models.models"]})
    print("connections:", connections.db_config.items())
    # env_initializer()
    user = UserSchemaCreate(username=os.environ.get("FIRST_SUPERUSER"), full_name="Administrator",
                            password=os.environ.get("FIRST_SUPERUSER_PASSWORD"))
    # test_app_with_db.post("/register", json=json)
    # hashed_password = get_password_hash(user.password)
    user = await functions.user.create_user(user)
    # frame = await Frame()
    # segments = await FrameSegment()
    # point = await FramePoint()
    yield user
    await connections.close_all()
    # await frame.fetch_related("cs_values", "frame_segments", "frame_points")
    # finalizer()


@pytest.fixture(scope="module")
@pytest.mark.asyncio
async def create_test_ship():
    ship = await Ship.create(**{"title": "TestPrep", "description": "for testing", "author_id": 1})
    # ship = await ShipSchema.from_tortoise_orm(ship)
    print(ship)
    yield ship
    await Ship.filter(id=ship.id).delete()


@pytest.fixture(scope="module")
@pytest.mark.asyncio
async def create_test_frame(create_test_ship):
    pos = random_pos()
    frame = await Frame.create(**{"frame_pos": pos, "ship_id": create_test_ship.id})
    # frame = await FrameSchema.from_tortoise_orm(frame)
    print(frame)
    yield frame
    await Frame.filter(id=frame.id).delete()


@pytest.fixture(scope="module")
@pytest.mark.asyncio
async def context():
    yield {}


@pytest.fixture(scope="module")
@pytest.mark.asyncio
async def superuser_token_headers(test_app_with_db: TestClient) -> Dict[str, str]:
    yield await get_superuser_token_headers(test_app_with_db)


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    try:
        loop = asyncio.get_running_loop()
        yield loop
    except RuntimeError as ex:
        print("Exception:", str(ex))
        if "no running event loop" in str(ex):
            print("start ne loop")
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            yield loop
    loop.close()


async def create_geometry() -> int:
    ship = await random_ship(1)
    frame = await random_frame(ship.id)
    # print(frame.id)
    p1 = FramePoint(frame_id=frame.id, y=0, z=0)
    await p1.save()
    p2 = FramePoint(frame_id=frame.id, y=12.5, z=0)
    await p2.save()
    p3 = FramePoint(frame_id=frame.id, y=25, z=0)
    await p3.save()
    p4 = FramePoint(frame_id=frame.id, y=0, z=2)
    await p4.save()
    p5 = FramePoint(frame_id=frame.id, y=2, z=2)
    await p5.save()
    p6 = FramePoint(frame_id=frame.id, y=12.5, z=2)
    await p6.save()
    p7 = FramePoint(frame_id=frame.id, y=23, z=2)
    await p7.save()
    p8 = FramePoint(frame_id=frame.id, y=25, z=2)
    await p8.save()
    p9 = FramePoint(frame_id=frame.id, y=0, z=17)
    await p9.save()
    p10 = FramePoint(frame_id=frame.id, y=2, z=17)
    await p10.save()
    p11 = FramePoint(frame_id=frame.id, y=23, z=17)
    await p11.save()
    p12 = FramePoint(frame_id=frame.id, y=25, z=17)
    await p12.save()
    # await FramePoint.bulk_create([p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12])
    # print(p1.id)
    await FrameSegment.bulk_create([
        FrameSegment(frame_id=frame.id, start_point_id=p3.id, end_point_id=p8.id, thick=0.02),
        FrameSegment(frame_id=frame.id, start_point_id=p2.id, end_point_id=p3.id, thick=0.02),
        FrameSegment(frame_id=frame.id, start_point_id=p8.id, end_point_id=p7.id, thick=0.02),
        FrameSegment(frame_id=frame.id, start_point_id=p1.id, end_point_id=p2.id, thick=0.02),
        FrameSegment(frame_id=frame.id, start_point_id=p7.id, end_point_id=p6.id, thick=0.02),
        FrameSegment(frame_id=frame.id, start_point_id=p6.id, end_point_id=p5.id, thick=0.02),
        FrameSegment(frame_id=frame.id, start_point_id=p5.id, end_point_id=p4.id, thick=0.02),
        FrameSegment(frame_id=frame.id, start_point_id=p4.id, end_point_id=p1.id, thick=0.02),
        FrameSegment(frame_id=frame.id, start_point_id=p5.id, end_point_id=p10.id, thick=0.02),
        FrameSegment(frame_id=frame.id, start_point_id=p10.id, end_point_id=p9.id, thick=0.02),
        FrameSegment(frame_id=frame.id, start_point_id=p9.id, end_point_id=p4.id, thick=0.02),
        FrameSegment(frame_id=frame.id, start_point_id=p8.id, end_point_id=p12.id, thick=0.02),
        FrameSegment(frame_id=frame.id, start_point_id=p12.id, end_point_id=p11.id, thick=0.02),
        FrameSegment(frame_id=frame.id, start_point_id=p11.id, end_point_id=p7.id, thick=0.02),
    ])
    return frame.id


@pytest.fixture()
@pytest.mark.asyncio
async def geometry_ready(test_app_with_db) -> int:
    # loop = asyncio._event_loop()
    # loop = asyncio.new_event_loop()
    # id = event_loop.run_until_complete(create_geometry())
    id = await create_geometry()
    yield id
    # asyncio.run(create_geometry())
