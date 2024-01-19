import pytest
from pytest import fixture
from hoc_crawler import crawl
from hoc_crawler.hoc_crawler import InvalidHOC, SupportsHOC, CrawlerError


@fixture
def func_all_invalid():
    def f(H, H_gw):
        raise InvalidHOC()

    return f


@fixture
def func_10_max():
    def f(H, H_gw):
        if H <= 10:
            return "OK"
        raise InvalidHOC()

    return f


@fixture
def func_10_max_2_no_good():
    def f(H, H_gw):
        if H <= 10:
            if H == 2:
                raise InvalidHOC()
            return "OK"
        raise InvalidHOC()

    return f


@fixture(
    params=[
        (dict(target="Max", flooded=True, hoc=(2, 9)), 9),
        (dict(target="Max", flooded=True, hoc=(2, 10)), 10),
        (dict(target="Max", flooded=True, hoc=(2, 11)), 10),
        (dict(target="Min", flooded=True, hoc=(1, 1)), 1),
        (dict(target="Min", flooded=True, hoc=(2, 1)), 1),
        (dict(target="Min", flooded=True, hoc=(2, 0)), 0),
    ]
)
def kwargs_and_result(request):
    return request.param


def test_crawl(func_10_max: SupportsHOC, kwargs_and_result):
    kwargs, result = kwargs_and_result
    assert crawl(func_10_max, **kwargs) == result


def test_crawl_invalid(func_all_invalid: SupportsHOC, kwargs_and_result):
    kwargs, _ = kwargs_and_result
    with pytest.raises(CrawlerError):
        crawl(func_all_invalid, **kwargs)


def test_crawl_forgiveness_1(func_10_max_2_no_good: SupportsHOC):
    assert crawl(func_10_max_2_no_good, target="Max", flooded=True, hoc=(1, 10), forgiveness_level=1) == 10


def test_crawl_forgiveness_0(func_10_max_2_no_good: SupportsHOC):
    assert crawl(func_10_max_2_no_good, target="Max", flooded=True, hoc=(1, 10), forgiveness_level=0) == 1
