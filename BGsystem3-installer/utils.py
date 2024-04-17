import os
import pathlib
from typing import Tuple


def ToAbsolutePath(path: str) -> str:
    return os.path.normpath(os.path.abspath(path)).__str__()


def JoinPath(path: str, *paths: Tuple[str]) -> str:
    return os.path.normpath(os.path.join(path, *paths)).__str__()


def ChangeSuffix(path: str, suffix: str) -> str:
    return pathlib.Path(path).with_suffix(suffix).__str__()


def ToParentPath(path: str) -> str:
    return JoinPath("virtual-folder", path)


def IfPathExist(path: str) -> bool:
    return os.path.exists(path)


def IfFileExist(path: str) -> bool:
    return os.path.isfile(path)
