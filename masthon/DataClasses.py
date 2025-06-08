"""
Some classes representing API objects here ! (And enums needed to use the package well)
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

import json

from .Exceptions import DataClassException


def _date_factory(arg: str | datetime) -> datetime:
    return (
        arg
        if isinstance(arg, datetime)
        else (
            datetime.fromisoformat(arg.replace("Z", "+00:00"))
            if isinstance(arg, str)
            else None
        )
    )


def _custom_object_factory(arg: Any, Type) -> Any:
    if isinstance(arg, Type) or arg is None:
        return arg
    else:
        return Type(**arg)


def _custom_list_objects_factory(arg: Any, Type) -> Any:
    if len(arg) < 1 or isinstance(arg[0], Type):
        return arg
    else:
        return [Type(**element) for element in arg]


# # ! Already deprecated, need big rework and fixes
# class DataClass:
#     """:)"""

#     def __repr__(self) -> str:
#         args = ", ".join(
#             [
#                 str(attr) + "=" + repr(self.__getattribute__(attr))
#                 for attr in self
#             ]
#         )
#         if len(args) > 76:
#             return f"""{self.__class__.__name__}({args[:40] + " ... " + args[-10:]})"""
#         else:
#             return f"""{self.__class__.__name__}({args})"""

#     # # TODO: Complete that
#     # #! Not working yet
#     # def __set(self, **kwargs):
#     #     ignored = {}
#     #     ann = self.__init__.__annotations__
#     #     self.__slots__ = frozenset()
#     #     for k, v in kwargs:
#     #         if k not in self.__annotations__.keys():
#     #             ignored[k] = v
#     #         else:
#     #             self.__slots__ += frozenset(k)
#     #             try:
#     #                 if isinstance(v, ann[k]):
#     #                     setattr(self, k, v)
#     #             except TypeError as e:
#     #                 if e.args.startswith("Subscripted "):  # typing
#     #                     pass
#     #                 else:
#     #                     raise e
#     #     if len(ignored) > 0:
#     #         raise DataClassException(json.dumps(ignored), ignored)


@dataclass(order=True)
class Emoji:
    shortcode: str
    url: str
    static_url: str
    visible_in_picker: bool


@dataclass(order=True)
class Field:
    name: str
    value: str
    verified_at: Optional[datetime | str] = None

    def __post_init__(self):
        self.verified_at = _date_factory(self.verified_at)


@dataclass(order=True)
class ImageMetaInfos:
    width: int
    height: int
    size: str
    aspect: float


@dataclass(order=True)
class Focus:
    x: float
    y: float


@dataclass(order=True)
class Meta:
    original: Dict[str, Any] | ImageMetaInfos
    small: Dict[str, Any] | ImageMetaInfos
    focus: Optional[Dict[str, float] | Focus] = None

    def __post_init__(self):
        self.focus = _custom_object_factory(self.focus, Focus)
        self.original = _custom_object_factory(self.original, ImageMetaInfos)
        self.small = _custom_object_factory(self.small, ImageMetaInfos)


@dataclass(order=True)
class Source:
    privacy: str
    sensitive: bool
    language: str
    note: str
    fields: List[Dict[str, Any] | Field]
    follow_requests_count: int

    def __post_init__(self):
        self.fields = _custom_list_objects_factory(self.fields)


@dataclass(order=True)
class Role:
    id: str
    name: str
    permissions: str
    color: str
    highlighted: bool


@dataclass(order=True)
class Account:
    id: str
    username: str
    acct: str
    url: str
    display_name: str
    note: str
    avatar: str
    avatar_static: str
    header: str
    header_static: str
    locked: bool
    fields: List[Dict[str, Any] | Field]
    emojis: List[Dict[str, Any] | Emoji]
    bot: bool
    created_at: str
    statuses_count: int
    followers_count: int
    following_count: int
    last_status_at: Optional[str] = None
    noindex: Optional[bool] = None
    moved: Optional[Dict[str, Any] | Account] = None
    suspended: Optional[bool] = None
    limited: Optional[bool] = None
    group: Optional[bool] = None
    discoverable: Optional[bool] = None
    attribution_domains: Optional[List[str]] = None
    source: Optional[Dict[str, Any] | Source] = None
    role: Optional[Dict[str, Any] | Role] = None
    mute_expires_at: Optional[str] = None
    indexable: Optional[bool] = None
    uri: Optional[str] = None
    hide_collections: Optional[Any] = None
    roles: Optional[List[Any]] = None

    def __post_init__(self):
        self.fields = _custom_list_objects_factory(self.fields, Field)
        self.emojis = _custom_list_objects_factory(self.emojis, Emoji)
        self.created_at = _date_factory(self.created_at)
        self.last_status_at = _date_factory(self.last_status_at)
        self.moved = _custom_object_factory(self.moved, Account)
        self.source = _custom_object_factory(self.source, Source)
        self.role = _custom_object_factory(self.role, Role)
        self.mute_expires_at = _date_factory(self.mute_expires_at)


@dataclass(order=True)
class Application:
    name: str
    website: Optional[str] = None


@dataclass(order=True)
class Mention:
    id: str
    username: str
    url: str
    acct: str


@dataclass(order=True)
class Tag:
    name: str
    url: str


@dataclass(order=True)
class MediaAttachment:
    id: str
    type: str
    url: str
    preview_url: str
    preview_remote_url: str
    meta: Dict[str, Any] | Meta
    text_url: Optional[str] = None
    remote_url: Optional[str] = None
    description: Optional[str] = None
    blurhash: Optional[str] = None

    def __post_init__(self):
        self.meta = _custom_object_factory(self.meta, Meta)


@dataclass(order=True)
class Poll:
    id: str
    expires_at: str
    expired: bool
    multiple: bool
    votes_count: int
    voters_count: int
    options: List[Dict[str, Any]]
    emojis: List[Dict[str, Any] | Emoji]
    voted: Optional[bool] = None

    def __post_init__(self):
        self.expires_at = _date_factory(self.expires_at)
        self.emojis = _custom_list_objects_factory(self.emojis, Emoji)


@dataclass(order=True)
class PreviewCard:
    url: str
    title: str
    description: str
    type: str
    author_name: str
    author_url: str
    provider_name: str
    provider_url: str
    html: str
    width: int
    height: int
    embed_url: str
    image: Optional[str] = None
    blurhash: Optional[str] = None


@dataclass(order=True)
class Status:
    id: str
    uri: str
    created_at: str
    account: Account | Dict[str, Any]
    content: str
    visibility: str
    sensitive: bool
    spoiler_text: str
    media_attachments: List[Dict[str, Any] | MediaAttachment]
    mentions: List[Dict[str, Any] | Mention]
    tags: List[Dict[str, Any] | Tag]
    emojis: List[Dict[str, Any] | Emoji]
    reblogs_count: int
    favourites_count: int
    replies_count: int
    application: Optional[Dict[str, Any] | Application] = None
    url: Optional[str] = None
    in_reply_to_id: Optional[str] = None
    in_reply_to_account_id: Optional[str] = None
    reblog: Optional["Status"] = None
    poll: Optional[Dict[str, Any] | Poll] = None
    card: Optional[Dict[str, Any] | PreviewCard] = None
    language: Optional[str] = None
    text: Optional[str] = None
    edited_at: Optional[str] = None
    favourited: Optional[bool] = None
    reblogged: Optional[bool] = None
    muted: Optional[bool] = None
    bookmarked: Optional[bool] = None
    pinned: Optional[bool] = None
    filtered: Optional[List[Dict[str, Any]]] = None
    quote: Optional[Any] = None

    def __post_init__(self):
        self.created_at = _date_factory(self.created_at)
        self.account = _custom_object_factory(self.account, Account)
        self.media_attachments = _custom_list_objects_factory(
            self.media_attachments, MediaAttachment
        )
        self.application = _custom_object_factory(self.application, Application)
        self.mentions = _custom_list_objects_factory(self.mentions, Mention)
        self.tags = _custom_list_objects_factory(self.tags, Tag)
        self.emojis = _custom_list_objects_factory(self.emojis, Emoji)
        self.poll = _custom_object_factory(self.poll, Poll)
        self.card = _custom_object_factory(self.card, PreviewCard)
        self.edited_at = _date_factory(self.edited_at)


# Enums


class RequestMethod(Enum):
    GET = "get"
    POST = "post"
    DELETE = "delete"
    PUT = "put"
    PATCH = "patch"


class Visibility(Enum):
    PUBLIC = "public"
    UNLISTED = "unlisted"
    PRIVATE = "private"
    DIRECT = "direct"
