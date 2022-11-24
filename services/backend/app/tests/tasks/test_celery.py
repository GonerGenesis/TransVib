import pytest
from fastapi import Depends

from app.core.config import get_settings
from app.db.models import FrameCSValues, FramePoint, Frame
from app.db.schemas import FramePointSchema, FrameSchema
import numpy as np
from tortoise import connections, Tortoise

pytestmark = pytest.mark.asyncio


# async def get_context(
#         settings=Depends(get_settings),
# ):
#     return {
#         'settings': settings
#     }

async def test_celery_running():
    from app.worker import test_celery
    test_string: str = "test"
    result = test_celery.apply_async((test_string,), queue='main-queue').get()
    print(result)
    assert result == f"test task return {test_string}"


async def test_celery_calcs(test_app_with_db, geometry_ready):
    from app.worker import calc_frame_properties
    print(f"going with frame:{geometry_ready}")
    # context = await get_context()
    # print(context['settings'].testing)
    # print(await FramePoint.filter(frame_id=geometry_ready).all())
    # print(await FrameSchema.from_queryset_single(Frame.get(id=geometry_ready)))
    r = calc_frame_properties.apply_async(args=[geometry_ready, 'test'], queue='main-queue')
    print(r.get())
    frame_props: FrameCSValues = await FrameCSValues.get(frame_id=geometry_ready)
    # print(r.get())
    print(repr(frame_props))
    print(frame_props.center)
    assert frame_props.frame_id == geometry_ready
    np.testing.assert_allclose(float(frame_props.area), 2.36)
    np.testing.assert_allclose(float(frame_props.center['y']), 12.5)
    np.testing.assert_allclose(float(frame_props.center['z']), 5.864407)
    np.testing.assert_allclose(float(frame_props.azzs), 74.86328)
    np.testing.assert_allclose(float(frame_props.ayys), 235.09)
    np.testing.assert_allclose(float(frame_props.ayzs), 0.0)
    np.testing.assert_allclose(float(frame_props.phi), 0.0)
    np.testing.assert_allclose(float(frame_props.i2), 74.86328)
    np.testing.assert_allclose(float(frame_props.i1), 235.09)
    np.testing.assert_allclose(float(frame_props.it), 8.498906)
    np.testing.assert_allclose(float(frame_props.shear_center['y']), 12.5)
    np.testing.assert_allclose(float(frame_props.shear_center['z']), 5.864407 - 11.14286453)
    np.testing.assert_allclose(float(frame_props.awwm), 7506.373)
