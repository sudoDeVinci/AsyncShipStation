from typing import TypedDict

from ..common import PackageGist


class PackageListResponse(TypedDict):
    packages: list[PackageGist]
