"""
Some classes representing API objects here ! (And enums needed to use the package well)
"""

from typing import (
    List,
    Optional,
    Dict,
    Any,
    Union,
    Self,
    Iterable,
    TypeAlias,
    Generic,
    TypeVar,
    Type,
)
import types
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

import json

from .Exceptions import DataClassException


def date_factory(arg: str | datetime) -> datetime:
    return (
        arg
        if isinstance(arg, datetime)
        else (
            datetime.fromisoformat(arg.replace("Z", "+00:00"))
            if isinstance(arg, str)
            else None
        )
    )


def custom_object_factory(arg: Any, Type) -> Any:
    if isinstance(arg, Type) or arg is None:
        return arg
    else:
        if not isinstance(Type, tuple):
            return Type(**arg)
        else:
            for CType in Type:
                try:
                    return CType(**arg)
                except TypeError:
                    continue


def custom_list_objects_factory(arg: Any, Type) -> Any:
    if len(arg) < 1 or isinstance(arg[0], Type):
        return arg
    else:
        return [Type(**element) for element in arg]


def convert_to_enum(arg: Any, enum: Any) -> Any:
    for el in enum:
        if el.value == arg:
            return el
    raise ValueError(f"`{arg}` is not a value of enum `{enum}`")


class __DETECTOR_CLS: ...


class DATE_(__DETECTOR_CLS): ...


class OBJECT_(__DETECTOR_CLS): ...


class ENUM_(__DETECTOR_CLS): ...


ID: TypeAlias = str
URL: TypeAlias = str
DATETIME: TypeAlias = str | datetime | DATE_

_APIO0 = TypeVar("_APIO0")
_ENUM = TypeVar("_ENUM")
API_OBJECT: TypeAlias = Dict[str, Any] | _APIO0 | OBJECT_
ENUM: TypeAlias = str | _ENUM | ENUM_



def customDC(cls):
    class _Wrapper(cls):
        __annotations__ = cls.__annotations__

        def __post_init__(self):
            for attr, annn in cls.__annotations__.items():
                if isinstance(annn, type(Union[int, str])):
                    if ENUM_ in annn.__args__:
                        self.__setattr__(
                            attr,
                            convert_to_enum(self.__getattribute__(attr), annn.__args__[1]),
                        )
                    if DATE_ in annn.__args__:
                        self.__setattr__(
                            attr,
                            date_factory(self.__getattribute__(attr)),
                        )
                    if OBJECT_ in annn.__args__:
                        self.__setattr__(
                            attr,
                            custom_object_factory(self.__getattribute__(attr), annn.__args__[1]),
                        )
                elif isinstance(annn, type(List[int])):
                    if isinstance(annn.__args__[0], type(Union[int, str])):
                        if ENUM_ in annn.__args__[0].__args__:
                            self.__setattr__(
                                attr,
                                [convert_to_enum(el, annn.__args__[0].__args__[1]) for el in self.__getattribute__(attr)],
                            )
                        if OBJECT_ in annn.__args__[0].__args__:
                            self.__setattr__(
                                attr,
                                custom_list_objects_factory(self.__getattribute__(attr), annn.__args__[0].__args__[1]),
                            )
        
        def __repr__(self):
            return super().__repr__().replace("customDC.<locals>._Wrapper(", cls.__name__ + "(")

    _Wrapper.__name__ = cls.__name__
    _Wrapper.__module__ = cls.__module__
    return _Wrapper


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


class MediaType(Enum):
    UNKNOWN = "unknown"
    IMAGE = "image"
    GIFV = "gifv"
    VIDEO = "video"
    AUDIO = "audio"


class PreviewCardType(Enum):
    LINK = "link"
    PHOTO = "photo"
    VIDEO = "video"
    RICH = "RICH"  #! Not currently accepted, so won’t show up in practice.


class Context(Enum):
    HOME = "home"
    NOTIFICATIONS = "notifications"
    PUBLIC = "public"
    THREAD = "thread"
    ACCOUNT = "account"


class FilterAction(Enum):
    WARN = "warn"
    HIDE = "hide"
    BLUR = "blur"


class QuoteState(Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    REVOKED = "revoked"
    DELETED = "deleted"
    UNAUTHORIZED = "unauthorized"


class ReportCategory(Enum):
    SPAM = "spam"
    VIOLATION = "violation"
    OTHER = "other"


class RelationshipSeveranceEventType(Enum):
    DOMAIN_BLOCK = "domain_block"
    USER_DOMAIN_BLOCK = "user_domain_block"
    ACCOUNT_SUSPENSION = "account_suspension"


class AppealState(Enum):
    APPROVED = "approved"
    REJECTED = "rejected"
    PENDING = "pending"


class WarningAction(Enum):
    NONE = "none"
    DISABLE = "disable"
    MARK_STATUSES_AS_SENSITIVE = "mark_statuses_as_sensitive"
    DELETE_STATUSES = "delete_statuses"
    SENSITIVE = "sensitive"
    SILENCE = "silence"
    SUSPEND = "suspend"


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

@customDC
@dataclass(order=True)
class Emoji:
    shortcode: str
    url: URL
    static_url: URL
    visible_in_picker: bool
    category: Optional[str] = None


@customDC
@dataclass(order=True)
class Field:
    name: str
    value: str
    verified_at: Optional[DATETIME] = None

    def __post_init__(self):
        self.verified_at = date_factory(self.verified_at)


@customDC
@dataclass(order=True)
class ImageMetaInfos:
    width: int
    height: int
    size: str
    aspect: float


@customDC
@dataclass(order=True)
class Focus:
    x: float
    y: float


@customDC
@dataclass(order=True)
class Meta:
    original: API_OBJECT[ImageMetaInfos]
    small: API_OBJECT[ImageMetaInfos]
    focus: Optional[API_OBJECT[Focus]] = None

    def __post_init__(self):
        self.focus = custom_object_factory(self.focus, Focus)
        self.original = custom_object_factory(self.original, ImageMetaInfos)
        self.small = custom_object_factory(self.small, ImageMetaInfos)


@customDC
@dataclass(order=True)
class Source:
    privacy: ENUM[Visibility]
    sensitive: bool
    language: str
    note: str
    fields: List[API_OBJECT[Field]]
    follow_requests_count: int

    def __post_init__(self):
        self.privacy = convert_to_enum(self.privacy, Visibility)
        self.fields = custom_list_objects_factory(self.fields)


@customDC
@dataclass(order=True)
class Role:
    id: ID
    name: str
    permissions: str
    color: str
    highlighted: bool


@customDC
@dataclass(order=True)
class Account:
    id: ID
    username: str
    acct: str
    url: URL
    display_name: str
    note: str
    avatar: URL
    avatar_static: URL
    header: URL
    header_static: URL
    locked: bool
    fields: List[API_OBJECT[Field]]
    emojis: List[API_OBJECT[Emoji]]
    bot: bool
    created_at: DATETIME
    statuses_count: int
    followers_count: int
    following_count: int
    last_status_at: Optional[DATETIME] = None
    noindex: Optional[bool] = None
    moved: Optional[API_OBJECT[Self]] = None
    suspended: Optional[bool] = None
    limited: Optional[bool] = None
    group: Optional[bool] = None
    discoverable: Optional[bool] = None
    attribution_domains: Optional[List[URL]] = None
    source: Optional[API_OBJECT[Source]] = None
    role: Optional[API_OBJECT[Role]] = None
    mute_expires_at: Optional[DATETIME] = None
    indexable: Optional[bool] = None
    uri: Optional[URL] = None
    hide_collections: Optional[bool] = None
    roles: Optional[List[API_OBJECT[Role]]] = None

    def __post_init__(self):
        self.fields = custom_list_objects_factory(self.fields, Field)
        self.emojis = custom_list_objects_factory(self.emojis, Emoji)
        self.created_at = date_factory(self.created_at)
        self.last_status_at = date_factory(self.last_status_at)
        self.moved = custom_object_factory(self.moved, Account)
        self.source = custom_object_factory(self.source, Source)
        self.role = custom_object_factory(self.role, Role)
        self.mute_expires_at = date_factory(self.mute_expires_at)


@customDC
@dataclass(order=True)
class Application:
    name: str
    scopes: Optional[List[str]] = None
    redirect_uris: Optional[List[URL]] = None
    website: Optional[URL] = None
    redirect_uri: Optional[URL] = None  #! deprecated
    vapid_key: Optional[str] = None  #! deprecated
    client_id: Optional[ID] = None  # from Credential app object
    client_secret: Optional[str] = None  # ''
    client_secret_expires_at: Optional[DATETIME | int] = (
        None  # '' #? 0 (added on 4.3.0))
    )


@customDC
@dataclass(order=True)
class Mention:
    id: ID
    username: str
    url: URL
    acct: str


@customDC
@dataclass(order=True)
class Tag:
    name: str
    url: URL


@customDC
@dataclass(order=True)
class MediaAttachment:
    id: ID
    type: ENUM[MediaType]
    url: URL
    preview_url: URL
    preview_remote_url: URL
    meta: API_OBJECT[Meta]
    text_url: Optional[URL] = None
    remote_url: Optional[URL] = None
    description: Optional[str] = None
    blurhash: Optional[str] = None

    def __post_init__(self):
        self.type = convert_to_enum(self.type, MediaType)
        self.meta = custom_object_factory(self.meta, Meta)


@customDC
@dataclass(order=True)
class Poll_Option:
    title: str
    votes_count: Optional[int]


@customDC
@dataclass(order=True)
class Poll:
    id: ID
    expires_at: DATETIME
    expired: bool
    multiple: bool
    votes_count: int
    voters_count: int
    options: List[API_OBJECT[Poll_Option]]
    emojis: List[API_OBJECT[Emoji]]
    voted: Optional[bool] = None

    def __post_init__(self):
        self.expires_at = date_factory(self.expires_at)
        self.options = custom_list_objects_factory(self.options, Poll_Option)
        self.emojis = custom_list_objects_factory(self.emojis, Emoji)


@customDC
@dataclass(order=True)
class PreviewCard:
    url: URL
    title: str
    description: str
    type: ENUM[PreviewCardType]
    author_name: str
    author_url: URL
    provider_name: str
    provider_url: URL
    html: str
    width: int
    height: int
    embed_url: URL
    image: Optional[str] = None
    blurhash: Optional[str] = None

    def __post_init__(self):
        self.type = convert_to_enum(self.type, PreviewCardType)


@customDC
@dataclass(order=True)
class Quote:
    state: ENUM[QuoteState]
    status: Optional[API_OBJECT["Status"]] = None

    def __post_init__(self):
        self.state = convert_to_enum(self.state, QuoteState)


@customDC
@dataclass(order=True)
class ShallowQuote:
    state: ENUM[QuoteState]
    status_id: Optional[ID] = None

    def __post_init__(self):
        self.state = convert_to_enum(self.state, QuoteState)


@customDC
@dataclass(order=True)
class FilterKeyword:
    id: ID
    keyword: str
    whole_word: bool


@customDC
@dataclass(order=True)
class FilterStatus:
    id: ID
    status_id: ID


@customDC
@dataclass(order=True)
class Filter:
    id: ID
    title: str
    context: List[ENUM[Context]]
    expires_at: Optional[DATETIME]
    filter_action: ENUM[FilterAction]
    keywords: List[FilterKeyword]
    statuses: List[FilterStatus]

    def __post_init__(self):
        self.context = [convert_to_enum(el, Context) for el in self.context]
        self.filter_action = convert_to_enum(self.filter_action, FilterAction)
        self.expires_at = date_factory(self.expires_at)
        self.keywords = custom_list_objects_factory(self.keywords, FilterKeyword)
        self.statuses = custom_list_objects_factory(self.statuses, FilterStatus)


@customDC
@dataclass(order=True)
class FilterResult:
    filter: Filter
    keyword_matches: Optional[List[str]]
    status_matches: Optional[List[str]]

    def __post_init__(self):
        self.filter = custom_object_factory(self.filter, Filter)


@customDC
@dataclass(order=True)
class Status:
    id: ID
    uri: URL
    created_at: DATETIME
    account: API_OBJECT[Account]
    content: str
    visibility: ENUM[Visibility]
    sensitive: bool
    spoiler_text: str
    media_attachments: List[API_OBJECT[MediaAttachment]]
    mentions: List[API_OBJECT[Mention]]
    tags: List[API_OBJECT[Tag]]
    emojis: List[API_OBJECT[Emoji]]
    reblogs_count: int
    favourites_count: int
    replies_count: int
    application: Optional[API_OBJECT[Application]] = None
    url: Optional[URL] = None
    in_reply_to_id: Optional[ID] = None
    in_reply_to_account_id: Optional[ID] = None
    reblog: Optional["Status"] = None
    poll: Optional[API_OBJECT[Poll]] = None
    card: Optional[API_OBJECT[PreviewCard]] = None
    language: Optional[str] = None
    text: Optional[str] = None
    edited_at: Optional[DATETIME] = None
    favourited: Optional[bool] = None
    reblogged: Optional[bool] = None
    muted: Optional[bool] = None
    bookmarked: Optional[bool] = None
    pinned: Optional[bool] = None
    filtered: Optional[List[API_OBJECT[FilterResult]]] = None
    quote: Optional[API_OBJECT[Quote | ShallowQuote]] = None

    def __post_init__(self):
        self.visibility = convert_to_enum(self.visibility, Visibility)
        self.created_at = date_factory(self.created_at)
        self.account = custom_object_factory(self.account, Account)
        self.media_attachments = custom_list_objects_factory(
            self.media_attachments, MediaAttachment
        )
        self.application = custom_object_factory(self.application, Application)
        self.mentions = custom_list_objects_factory(self.mentions, Mention)
        self.tags = custom_list_objects_factory(self.tags, Tag)
        self.emojis = custom_list_objects_factory(self.emojis, Emoji)
        self.poll = custom_object_factory(self.poll, Poll)
        self.card = custom_object_factory(self.card, PreviewCard)
        self.edited_at = date_factory(self.edited_at)
        self.filtered = custom_list_objects_factory(self.filtered, FilterResult)
        self.quote = custom_object_factory(self.quote, (Quote, ShallowQuote))


@customDC
@dataclass
class Report:
    id: ID
    action_taken: bool
    action_taken_at: Optional[DATETIME]
    category: ENUM[ReportCategory]
    comment: str
    forwarded: bool
    created_at: DATETIME
    status_ids: Optional[List[ID]]
    rule_ids: Optional[List[ID]]
    target_account: API_OBJECT[Account]

    def __post_init__(self):
        self.action_taken_at = date_factory(self.action_taken_at)
        self.category = custom_object_factory(self.category, ReportCategory)
        self.created_at = date_factory(self.created_at)
        self.target_account = custom_object_factory(self.target_account, Account)


@customDC
@dataclass
class RelationshipSeveranceEvent:
    id: ID
    type: ENUM[RelationshipSeveranceEventType]
    purged: bool
    target_name: str
    followers_count: int
    following_count: int
    created_at: DATETIME

    def __post_init__(self):
        self.type = convert_to_enum(self.type, RelationshipSeveranceEventType)
        self.created_at = date_factory(self.created_at)


@customDC
@dataclass
class Appeal:
    text: str
    state: ENUM[AppealState]

    def __post_init__(self):
        self.state = convert_to_enum(self.state, AppealState)


@customDC
@customDC
@dataclass
class AccountWarning:
    id: ID
    action: ENUM[WarningAction]
    text: str
    status_ids: Optional[List[ID]]
    target_account: API_OBJECT[Account]
    appeal: Optional[API_OBJECT[Appeal]]
    created_at: DATETIME

    def __post_init__(self):
        self.action = convert_to_enum(self.action, WarningAction)
        self.appeal = custom_object_factory(self.appeal, Appeal)
        self.created_at = date_factory(self.created_at)


@customDC
@dataclass
class Notification:
    id: ID
    type: ENUM[NotificationType]
    group_key: str
    created_at: DATETIME
    account: API_OBJECT[Account]
    status: Optional[API_OBJECT[Status]] = None
    report: Optional[API_OBJECT[Report]] = None
    event: Optional[API_OBJECT[RelationshipSeveranceEvent]] = None
    moderation_warning: Optional[API_OBJECT[AccountWarning]] = None

    def __post_init__(self):
        self.type = convert_to_enum(self.type, NotificationType)
        self.created_at = date_factory(self.created_at)
        self.account = custom_object_factory(self.account, Account)
        self.report = custom_object_factory(self.report, Report)
        self.event = custom_object_factory(self.event, RelationshipSeveranceEvent)
        self.status = custom_object_factory(self.status, Status)
        self.moderation_warning = custom_object_factory(
            self.moderation_warning, AccountWarning
        )


@customDC
@dataclass
class Marker:
    last_read_id: ID
    version: int
    updated_at: DATETIME

    def __post_init__(self):
        self.updated_at = date_factory(self.updated_at)
