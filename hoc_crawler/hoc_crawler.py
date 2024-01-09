"""Figure out the height of cover limits for buried pipes."""

__version__ = "0.0.1"

from enum import StrEnum, auto
from typing import Protocol
from pint import Quantity
from .hoc_range import HOCRange, hoc_range


class CrawlerError(Exception):
    pass


class InvalidHOC(CrawlerError):
    pass


class SupportsHOC(Protocol):
    def __call__(self, H: Quantity|float, H_gw: Quantity|float, *args, **kwargs):
        ...


class TargetHOC(StrEnum):
    min = auto()
    max = auto()


def crawl(
    func: SupportsHOC,
    target: TargetHOC|str,
    flooded: bool = False,
    hoc: tuple[int|float|None]|HOCRange|None = None,
    *args,
    **kwargs,
) -> float:
    """Attempts different cover heights until the limit (max or min) is identified.

    Units assumed to be feet unless otherwise specified.
    """

    match target:
        case TargetHOC():
            pass
        case str():
            target = TargetHOC(target.lower())
        case _:
            raise CrawlerError(f"target type must be str ('min' or 'max') or TargetHOC, not {type(target).__name__}")

    match hoc:
        case None:
            hoc = hoc_range()
        case HOCRange():
            pass
        case (*hoc,):
            hoc = hoc_range(*hoc)
        case value:
            hoc = hoc_range(value)

    iter_hoc = {target.max:hoc.iter_up(), target.min:hoc.iter_down()}[target]
    prev_hoc = None

    for h in iter_hoc:
        kwargs["H"] = h
        if flooded:
            kwargs["H_gw"] = h

        try:
            func(*args, **kwargs)
        except InvalidHOC:
            break
        else:
            prev_hoc = h

    if prev_hoc is not None:
        return prev_hoc
    else:
        raise CrawlerError(f"failed to successfully determine {target} height of cover.")
