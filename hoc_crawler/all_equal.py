from typing import Collection

_NO_ARG = object()


def all_equal(collection: Collection, *ignore) -> bool:
    """Determine if all the values in a collection are equal. If values are supplied for ignore, they're ignored.

    NOTE: does NOT work for generators/iterators. Only collections.
    """

    gen = iter(collection)
    if ignore:
        return all(
            v == first
            for v in gen
            for first in gen
            if v not in ignore
            if first not in ignore
        )
    else:
        return all(v == first for v in gen for first in gen)
