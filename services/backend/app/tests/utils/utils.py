import random
import string
from typing import Dict

from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.core.config import get_settings
from app.db.models import FramePoint, Ship, Frame, FrameSegment


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_id() -> int:
    return random.randint(1, 250)


def random_pos() -> float:
    return round(random.uniform(0, 500), 3)


async def random_point(frame_id: int) -> FramePoint:
    return await FramePoint.create(y=random_pos(), z=random_pos(), frame_id=frame_id)

async def random_segment(frame_id: int) -> FrameSegment:
    p1 = await random_point(frame_id)
    p2 = await random_point(frame_id)
    return await FrameSegment.create(start_point=p1, end_point=p2, frame_id=frame_id, thick=random_pos())

async def random_ship(user_id: int) -> Ship:
    return await Ship.create(title=random_lower_string(), description=random_lower_string(), author_id=user_id)


async def random_frame(ship_id: int) -> Frame:
    return await Frame.create(frame_pos=random_pos(), ship_id=ship_id)


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


async def get_superuser_token_headers(client: AsyncClient) -> Dict[str, str]:
    login_data = {
        "username": get_settings().FIRST_SUPERUSER,
        "password": get_settings().FIRST_SUPERUSER_PASSWORD,
    }
    # print(login_data)
    r = await client.post("/login/access-token", data=login_data)
    tokens = r.json()
    # print("tokens", tokens)
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    #  print(headers)
    return headers
