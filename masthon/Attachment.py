from typing import Dict, Literal, Union


class Meta:
    __slots__ = ("focus", "original", "small")

    def __init__(
        self,
        focus: Dict[Literal["x", "y"], float],
        original: Dict[
            Literal["width", "height", "size", "aspect"],
            Union[int, int, str, float]
        ],
        small: Dict[
            Literal["width", "height", "size", "aspect"],
            Union[int, int, str, float]
        ],
    ):
        self.focus = focus
        self.original = original
        self.small = small


class Attachement:
    __slots__ = (
        "id",
        "type",
        "url",
        "preview_url",
        "remote_url",
        "text_url",
        "meta",
        "description",
        "blurhash",
    )

    def __init__(
        self,
        id_: str,
        type_: str,
        url: str,
        preview_url: str,
        remote_url: str,
        text_url: str,
        meta: Meta,
        description: str,
        blurhash: str,
    ):
        self.id = id_
        self.type = type_
        self.url = url
        self.preview_url = preview_url
        self.remote_url = remote_url
        self.text_url = text_url
        self.meta = meta
        self.description = description
        self.blurhash = blurhash
