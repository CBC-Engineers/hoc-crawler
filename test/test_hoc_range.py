import pytest
from pytest import fixture
from hoc_crawler.hoc_range import hoc_range, HOCRangeError
from pint import UnitRegistry

U = UnitRegistry()


@fixture(
    params=[
        (),
        (1.0,),
        (1.0, 1.0),
        (1.0, 1.0, 1.0),
        (1.0 * U.ft, 1.0 * U.ft, 1.0 * U.ft),
        (1.0 * U.ft, 1.0 * U.ft, 1.0),
        (1.0 * U.ft, 1.0, 1.0),
    ]
)
def args(request):
    return request.param


def test_hoc_range(args):
    assert hoc_range(*args)


@fixture(
    params=[
        (-1.0,),
        (1.0, -1.0),
        (1.0, 1.0, -1.0),
        (1.0 * U.ft, 1.0 * U.m, 1.0),
    ]
)
def bad_args(request):
    return request.param


def test_hoc_range_negative_args(bad_args):
    with pytest.raises(HOCRangeError):
        hoc_range(*bad_args)
