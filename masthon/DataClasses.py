"""
Some classes representing API objects here ! (And enums needed to use the package well)
"""

from typing import (
    List,
    Optional,
    Dict,
    Any,
    Union,
    Iterable,
    TypeAlias,
    TypeVar,
    Type,
    TYPE_CHECKING,
)
import types
from dataclasses import dataclass
from enum import Enum, EnumType
from datetime import datetime


from .Exceptions import DataClassException


def date_factory(arg: str | datetime) -> Optional[datetime]:
    return (
        arg
        if isinstance(arg, datetime)
        else (
            datetime.fromisoformat(arg.replace("Z", "+00:00"))
            if isinstance(arg, str)
            else None
        )
    )


def date_list_factory(arg: List[str | datetime]) -> List[Optional[datetime]]:
    return [date_factory(element) for element in arg]


TYPE_TVAR = TypeVar("TYPE_TVAR", bound=Type)
ENUM_TVAR = TypeVar("ENUM_TVAR", bound=EnumType)


def custom_object_factory(arg: Any, Type: TYPE_TVAR) -> Optional[TYPE_TVAR]:
    if arg is None:
        return None
    elif isinstance(Type, str):
        return globals()[Type](**arg)
    elif isinstance(arg, Type):
        return arg
    else:
        if not isinstance(Type, (tuple, type(Union[int, str]))):
            return Type(**arg)
        else:
            Types: tuple
            if isinstance(Type, tuple):
                Types = Type
            elif isinstance(Type, str):
                Types = Type
            else:
                if not TYPE_CHECKING:  # Mypy stop, #! Please let it here
                    Types = Type.__args__  # ? He does'nt love this statement
            for CType in Types:
                try:
                    return CType(**arg)
                except TypeError:
                    continue
            raise TypeError


def custom_list_objects_factory(arg: Any, Type: TYPE_TVAR) -> List[Optional[TYPE_TVAR]]:
    return [custom_object_factory(element, Type) for element in arg]


def convert_to_enum(arg: Any, Enum_: ENUM_TVAR) -> ENUM_TVAR:
    if not TYPE_CHECKING:
        return Enum_(arg)
    raise Exception("Mypy CRAP")


def convert_to_list_enum(arg: Any, Enum: ENUM_TVAR) -> List[ENUM_TVAR]:
    return [convert_to_enum(element, Enum) for element in arg]


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


def APIDATACLASS(cls):
    def set_attr(s, attr, func, *args):
        s.__setattr__(
            attr,
            func(s.__getattribute__(attr), *args),
        )

    class _Wrapper(cls):
        __annotations__ = cls.__annotations__

        def __post_init__(self):
            for attr, annn in cls.__annotations__.items():
                try:
                    if (
                        isinstance(annn, type(Union[int, str]))
                        and annn.__args__[1] is not types.NoneType
                    ):
                        if ENUM_ in annn.__args__:
                            set_attr(self, attr, convert_to_enum, annn.__args__[1])
                        elif DATE_ in annn.__args__:
                            set_attr(self, attr, date_factory)
                        elif OBJECT_ in annn.__args__:
                            set_attr(
                                self, attr, custom_object_factory, annn.__args__[1]
                            )
                    elif (
                        isinstance(annn, type(Union[int, str]))
                        and annn.__args__[1] is not types.NoneType
                        and isinstance(annn.__args__[0], type(List[int]))
                        and isinstance(
                            annn.__args__[0].__args__[0], type(Union[int, str])
                        )
                    ):
                        if ENUM_ in annn.__args__[0].__args__[0].__args__:
                            set_attr(
                                self,
                                attr,
                                convert_to_list_enum,
                                annn.__args__[0].__args__[0].__args__[1],
                            )
                        elif OBJECT_ in annn.__args__[0].__args__[0].__args__:
                            set_attr(
                                self,
                                attr,
                                custom_list_objects_factory,
                                annn.__args__[0].__args__[0].__args__[1],
                            )
                    elif isinstance(annn, type(List[int])) and isinstance(
                        annn.__args__[0], type(Union[int, str])
                    ):
                        if ENUM_ in annn.__args__[0].__args__:
                            set_attr(
                                self,
                                attr,
                                convert_to_list_enum,
                                annn.__args__[0].__args__[1],
                            )
                        elif OBJECT_ in annn.__args__[0].__args__:
                            set_attr(
                                self,
                                attr,
                                custom_list_objects_factory,
                                annn.__args__[0].__args__[1],
                            )
                except Exception as e:
                    raise DataClassException(
                        " ".join(
                            (f"Attribute: {attr}, Annotation: {annn}  |>\n", *e.args)
                        )
                    )

        def __repr__(self):
            return (
                super()
                .__repr__()
                .replace("APIDATACLASS.<locals>._Wrapper(", cls.__name__ + "(")
            )

    _Wrapper.__name__ = cls.__name__
    _Wrapper.__module__ = cls.__module__
    _Wrapper.__doc__ = cls.__doc__
    return _Wrapper


# Enums
class On(Enum): # not really used but I keep the idea
    START = "start"
    STOP = "stop"
    LOOP_STEP = "loop_step"
    REQUEST = "request"
    CHECK_EVENT = "check_event"
    POST_STATUS = "post_status"

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
    RICH = "RICH"  # mdoc: Not currently accepted, so won’t show up in practice.


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


# DATACLASSES


@APIDATACLASS
@dataclass(order=True)
class Emoji:
    shortcode: str
    url: URL
    static_url: URL
    visible_in_picker: bool
    category: Optional[str] = None

    def __post_init__(self):
        super().__post_init__()


@APIDATACLASS
@dataclass(order=True)
class Field:
    name: str
    value: str
    verified_at: Optional[DATETIME] = None

    def __post_init__(self):
        super().__post_init__()


@APIDATACLASS
@dataclass(order=True)
class ImageMetaInfos:
    width: int
    height: int
    size: str
    aspect: float

    def __post_init__(self):
        super().__post_init__()


@APIDATACLASS
@dataclass(order=True)
class Focus:
    x: float
    y: float

    def __post_init__(self):
        super().__post_init__()


@APIDATACLASS
@dataclass(order=True)
class Meta:
    original: API_OBJECT[ImageMetaInfos]
    small: API_OBJECT[ImageMetaInfos]
    focus: Optional[API_OBJECT[Focus]] = None

    def __post_init__(self):
        super().__post_init__()


@APIDATACLASS
@dataclass(order=True)
class Source:
    privacy: ENUM[Visibility]
    sensitive: bool
    language: str
    note: str
    fields: List[API_OBJECT[Field]]
    follow_requests_count: int

    def __post_init__(self):
        super().__post_init__()


@APIDATACLASS
@dataclass(order=True)
class Role:
    id: ID
    name: str
    permissions: str
    color: str
    highlighted: bool

    def __post_init__(self):
        super().__post_init__()


@APIDATACLASS
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
    moved: Optional[API_OBJECT["Account"]] = None
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
        super().__post_init__()


@APIDATACLASS
@dataclass(order=True)
class Application:
    name: str
    scopes: Optional[List[str]] = None
    redirect_uris: Optional[List[URL]] = None
    website: Optional[URL] = None
    redirect_uri: Optional[URL] = None  # mDOC: deprecated
    vapid_key: Optional[str] = None  # mDOC: deprecated
    client_id: Optional[ID] = None  # from Credential app object
    client_secret: Optional[str] = None  # ''
    client_secret_expires_at: Optional[DATETIME | int] = (
        None  # '' #? 0 (added on 4.3.0))
    )

    def __post_init__(self):
        super().__post_init__()


@APIDATACLASS
@dataclass(order=True)
class Mention:
    id: ID
    username: str
    url: URL
    acct: str

    def __post_init__(self):
        super().__post_init__()


@APIDATACLASS
@dataclass(order=True)
class Tag:
    name: str
    url: URL

    def __post_init__(self):
        super().__post_init__()


@APIDATACLASS
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
        super().__post_init__()


@APIDATACLASS
@dataclass(order=True)
class Poll_Option:
    title: str
    votes_count: Optional[int]

    def __post_init__(self):
        super().__post_init__()


@APIDATACLASS
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
        super().__post_init__()


@APIDATACLASS
@dataclass(order=True)
class PreviewCardAuthor:
    name: str
    url: URL
    account: Optional[API_OBJECT[Account]] = None

    def __post_init__(self):
        super().__post_init__()


@APIDATACLASS
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
    authors: Optional[List[API_OBJECT[PreviewCardAuthor]]] = None
    image: Optional[str] = None
    blurhash: Optional[str] = None
    language: Optional[str] = None

    def __post_init__(self):
        super().__post_init__()


@APIDATACLASS
@dataclass(order=True)
class Quote:
    state: ENUM[QuoteState]
    status: Optional[API_OBJECT["Status"]] = None

    def __post_init__(self):
        super().__post_init__()


@APIDATACLASS
@dataclass(order=True)
class ShallowQuote:
    state: ENUM[QuoteState]
    status_id: Optional[ID] = None

    def __post_init__(self):
        super().__post_init__()


@APIDATACLASS
@dataclass(order=True)
class FilterKeyword:
    id: ID
    keyword: str
    whole_word: bool

    def __post_init__(self):
        super().__post_init__()


@APIDATACLASS
@dataclass(order=True)
class FilterStatus:
    id: ID
    status_id: ID

    def __post_init__(self):
        super().__post_init__()


@APIDATACLASS
@dataclass(order=True)
class Filter:
    id: ID
    title: str
    context: List[ENUM[Context]]
    expires_at: Optional[DATETIME]
    filter_action: ENUM[FilterAction]
    keywords: List[API_OBJECT[FilterKeyword]]
    statuses: List[API_OBJECT[FilterStatus]]

    def __post_init__(self):
        super().__post_init__()


@APIDATACLASS
@dataclass(order=True)
class FilterResult:
    filter: Filter
    keyword_matches: Optional[List[str]]
    status_matches: Optional[List[str]]

    def __post_init__(self):
        super().__post_init__()


@APIDATACLASS
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
        super().__post_init__()


@APIDATACLASS
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
        super().__post_init__()


@APIDATACLASS
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
        super().__post_init__()


@APIDATACLASS
@dataclass
class Appeal:
    text: str
    state: ENUM[AppealState]

    def __post_init__(self):
        super().__post_init__()


@APIDATACLASS
@APIDATACLASS
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
        super().__post_init__()


@APIDATACLASS
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
        super().__post_init__()


@APIDATACLASS
@dataclass
class Marker:
    last_read_id: ID
    version: int
    updated_at: DATETIME

    def __post_init__(self):
        super().__post_init__()
