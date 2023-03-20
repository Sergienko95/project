from functools import partial
from pathlib import Path

_this_file = Path(__file__)

_resolved = False

DIR_PROJECT = _this_file.parent
DIR_REPO = DIR_PROJECT.parent
DIR_ARTIFACTS = DIR_REPO / ".artifacts"


def _resolve() -> None:
    global _resolved
    if _resolved:
        return

    import sys

    this_module = sys.modules[__name__]

    names = dir(this_module)
    _getattr = partial(getattr, this_module)
    namespace = zip(names, map(_getattr, names))
    paths = filter(lambda _pair: isinstance(_pair[1], Path), namespace)

    for name, obj in paths:
        obj = obj.resolve()
        setattr(this_module, name, obj)

    _resolved = True


_resolve()

__all__ = (
    "DIR_ARTIFACTS",
    "DIR_PROJECT",
    "DIR_REPO",
)
