from dataclasses import dataclass
from typing import overload


class HOCRangeError(Exception):
    pass


@dataclass
class HOCRange:
    """Represents a range of cover heights. The range is inclusive."""

    start: float = 1.0
    stop: float | None = None
    step: float = 1.0

    def iter_up(self):
        """Iterate upwards from starting value.

        The final value is the stop value unless there isn't a stop value, in which case the iterator is infinite.
        """

        value = self.start
        step = self.step
        stop = self.stop

        if self.stop is not None:
            while value < stop:
                yield value
                value += step
            else:
                yield stop
        else:
            while True:
                yield value
                value += step

    def iter_down(self):
        """Iterate downwards from starting value.

        The final value is the stop value unless there isn't a stop value, in which case the iterator is infinite.
        """

        value = self.start
        step = self.step
        stop = self.stop

        if stop is not None:
            while value > stop:
                yield value
                value -= step
            else:
                yield stop
        else:
            while True:
                yield value
                value -= step


@overload
def hoc_range() -> HOCRange:
    ...


@overload
def hoc_range(stop: float | None) -> HOCRange:
    ...


@overload
def hoc_range(start: float | None, stop: float | None):
    ...


@overload
def hoc_range(start: float | None, stop: float | None, step: float | None):
    ...


def hoc_range(*args) -> HOCRange:
    """Create a HOCRange. Floats are allowed. Negative values not allowed. Units optional.

    Can be called much like the range() function, but behaves differently. Main differences:
    1. None is allowed for any argument.
    2. The range is inclusive.

    The default start and step are both 1.0.
    """

    match args:
        case ():
            start, step, stop = 1.0, 1.0, None
        case (start,) if _check("start", start):
            step, stop = 1.0, None
        case (start, stop) if _check("start", start) and _check("stop", stop):
            step = 1.0
        case (start, step, stop) if _check("start", start) and _check(
            "step", step
        ) and _check("stop", stop):
            pass
        case _:
            raise HOCRangeError("Invalid arguments.")
    return HOCRange(start, stop, step)


def _check(arg_name, value):
    """Check hoc_range arguments for validity."""

    try:
        if value is None or value >= 0:
            return True
        return False
    except:
        raise HOCRangeError(
            f"numerical values are required, {arg_name}={type(value).__name__} not supported"
        )
