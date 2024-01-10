"""Figure out the height of cover limits for buried pipes."""

__version__ = "0.1.0"

from .hoc_crawler import crawl, TargetHOC, InvalidHOC
from .hoc_range import hoc_range

max = TargetHOC.max
min = TargetHOC.min
