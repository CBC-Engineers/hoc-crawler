# hoc_crawler
Figure out the height of cover limits (for buried pipes).

## Usage
Iterate over heights of cover, inclusively. `range` isn't so great because it doesn't allow for inclusivity or for 
open-ended ranges.

Example usage:

```python
from hoc_crawler import crawl, InvalidHOC

def my_pipe_cover_check(H):
    if H <= 10:
        return "OK"
    raise InvalidHOC(f"{H} is too much")

max_cover = crawl(my_pipe_cover_check, target="Max")
```

The maximum cover height will be returned as 10.
