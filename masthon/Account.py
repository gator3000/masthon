from typing import List
from .entities import *

from .Emoji import Emoji
from .Field import Field


class Account:
    __slots__ = (
        "id_",
        "username",
        "aact",
        "url",
        "display_name",
        "note",
        "avatar",
        "avatar_static",
        "header",
        "header_static",
        "locked",
        "fields",
        "emojis",
        "bot",
        "created_at",
        "last_status_at",
        "statuses_count",
        "followers_count",
        "following_count",
        "noindex",
        "moved",
        "suspended",
        "limited",
        "group",
        "discoverable",
    )

    def __init__(
        self,
        id_: str,
        username: str,
        aact: str,
        url: str,
        display_name: str,
        note: str,
        avatar: str,
        avatar_static: str,
        header: str,
        header_static: str,
        locked: bool,
        fields: List[Field],
        emojis: List[Emoji],
        bot: bool,
        created_at: str,
        last_status_at: str,
        statuses_count: int,
        followers_count: int,
        following_count: int,
        noindex: bool = None,
        moved: Account = None,
        suspended: bool = None,
        limited: bool = None,
        group=None,
        discoverable: bool = None,
    ):
        self.id = id_
        self.username = username
        self.aact = aact
        self.url = url
        self.display_name = display_name
        self.note = note
        self.avatar = avatar
        self.avatar_static = avatar_static
        self.header = header
        self.header_static = header_static
        self.locked = locked
        self.fields = fields
        self.emojis = emojis
        self.bot = bot
        self.created_at = created_at
        self.last_status_at = last_status_at
        self.statuses_count = statuses_count
        self.followers_count = followers_count
        self.following_count = following_count
        self.noindex = noindex
        self.moved = moved
        self.suspended = suspended
        self.limited = limited
        self.group = group
        self.discoverable = discoverable
