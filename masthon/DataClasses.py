"""
Some classes representing API objects here ! (And enums needed to use the package well)
"""

from typing import List, Optional, Dict, Any, Union, Self
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


def _convert_to_enum(arg: Any, enum: Any) -> Any:
    for el in enum:
        if el.value == arg:
            return el
    raise ValueError(f"`{arg}` is not a value of enum `{enum}`")


# # ! Already deprecated, need big rework and fixes, instead use @dataclass
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
    verified_at: Optional[str | datetime] = None

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
    created_at: str | datetime
    statuses_count: int
    followers_count: int
    following_count: int
    last_status_at: Optional[str | datetime] = None
    noindex: Optional[bool] = None
    moved: Optional[Dict[str, Any] | Self] = None
    suspended: Optional[bool] = None
    limited: Optional[bool] = None
    group: Optional[bool] = None
    discoverable: Optional[bool] = None
    attribution_domains: Optional[List[str]] = None
    source: Optional[Dict[str, Any] | Source] = None
    role: Optional[Dict[str, Any] | Role] = None
    mute_expires_at: Optional[str | datetime] = None
    indexable: Optional[bool] = None
    uri: Optional[str] = None
    hide_collections: Optional[bool] = None
    roles: Optional[List[Dict[str, Any] | Role]] = None

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
class Poll_Option:
    title: str
    votes_count: Optional[int]

@dataclass(order=True)
class Poll:
    id: str
    expires_at: str | datetime
    expired: bool
    multiple: bool
    votes_count: int
    voters_count: int
    options: List[Dict[str, Any] | Poll_Option]
    emojis: List[Dict[str, Any] | Emoji]
    voted: Optional[bool] = None

    def __post_init__(self):
        self.expires_at = _date_factory(self.expires_at)
        self.options = _custom_list_objects_factory(self.options, Poll_Option)
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
class Quote:
    state: str
    status: Optional[Dict[str, Any] | "Status"] = None


@dataclass(order=True)
class Status:
    id: str
    uri: str
    created_at: str | datetime
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
    filtered: Optional[List[Dict[str, Any]]] = None # TODO: /!\ ADD Support for theses objects
    quote: Optional[Quote] = None

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


@dataclass
class Report:
    id: str
    action_taken: bool
    action_taken_at: Optional[str | datetime]
    category: str
    comment: str
    forwarded: bool
    created_at: str | datetime
    status_ids: Optional[List[str]]
    rule_ids: Optional[List[str]]
    target_account: Dict[str, Any] | Account

    def __post_init__(self):
        self.action_taken_at = _date_factory(self.action_taken_at)
        self.created_at = _date_factory(self.created_at)
        self.target_account = _custom_object_factory(self.target_account, Account)


@dataclass
class RelationshipSeveranceEvent:
    id: str
    type: str
    purged: bool
    target_name: str
    followers_count: int
    following_count: int
    created_at: str | datetime

    def __post_init__(self):
        self.created_at = _date_factory(self.created_at)


@dataclass
class Appeal:
    text: str
    state: str


@dataclass
class AccountWarning:
    id: str
    action: str
    text: str
    status_ids: Optional[List[str]]
    target_account: Dict[str, Any] | Account
    appeal: Optional[Dict[str, Any] | Appeal]
    created_at: str | datetime

    def __post_init__(self):
        self.appeal = _custom_object_factory(self.appeal, Appeal)
        self.created_at = _date_factory(self.created_at)


@dataclass
class Notification:
    id: str
    type: str
    group_key: str
    created_at: str | datetime
    account: Dict[str, Any] | Account
    status: Optional[Dict[str, Any] | Status] = None
    report: Optional[Dict[str, Any] | Report] = None
    event: Optional[Dict[str, Any] | RelationshipSeveranceEvent] = None
    moderation_warning: Optional[Dict[str, Any] | AccountWarning] = None

    def __post_init__(self):
        self.type = _convert_to_enum(self.type, NotificationType)
        self.created_at = _date_factory(self.created_at)
        self.account = _custom_object_factory(self.account, Account)
        self.report = _custom_object_factory(self.report, Report)
        self.event = _custom_object_factory(self.event, RelationshipSeveranceEvent)
        self.status = _custom_object_factory(self.status, Status)
        self.moderation_warning = _custom_object_factory(
            self.moderation_warning, AccountWarning
        )

@dataclass
class Marker:
    last_read_id: str
    version: int
    updated_at: str | datetime

    def __post_init__(self):
        self.updated_at = _date_factory(self.updated_at)

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


class Event(Enum):
    UNREAD_NOTIFICATION = "unread_notification"
    NEW_MENTION = "new_mention"


class EventStatus(Enum):
    TRIGGERED = "triggered"
    NONE = "none"
    ERROR = "error"


class NotificationType(Enum):
    MENTION = "mention"
    STATUS = "status"
    REBLOG = "reblog"
    FOLLOW = "follow"
    FOLLOW_REQUEST = "follow_request"
    FAVOURITE = "favourite"
    POLL = "poll"
    UPDATE = "update"
    ADMIN_SIGN_UP = "admin.sign_up"
    ADMIN_REPORT = "admin.report"

class TimelineType(Enum):
    HOME = "home"
    NOTIFICATIONS = "notifications"