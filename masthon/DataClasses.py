from typing import List, Optional, Dict, Any, Union
from datetime import datetime

import json

from .Exceptions import DataClassException


class DataClass:
    def __repr__(self) -> str:
        return f"""{self.__class__.__name__}({(", ".join(
            [
                repr(attr) + "=" + repr(self.__getattribute__(attr))
                for attr in self.__slots__
            ]
        ))})"""

    # TODO: Complete that
    #! Not working yet
    def __set(self, **kwargs):
        ignored = {}
        ann = self.__init__.__annotations__
        self.__slots__ = frozenset()
        for k, v in kwargs:
            if k not in self.__annotations__.keys():
                ignored[k] = v
            else:
                self.__slots__ += frozenset(k)
                try:
                    if isinstance(v, ann[k]):
                        setattr(self, k, v)
                except TypeError as e:
                    if e.args.startswith("Subscripted "): # typing
                        pass
                    else:
                        raise e
        if len(ignored) > 0:
            raise DataClassException(json.dumps(ignored), ignored)


class Emoji(DataClass):
    __slots__ = ("shortcode", "url", "static_url", "visible_in_picker")

    def __init__(
        self, shortcode: str, url: str, static_url: str, visible_in_picker: bool
    ):
        self.shortcode = shortcode
        self.url = url
        self.static_url = static_url
        self.visible_in_picker = visible_in_picker


class Field(DataClass):
    __slots__ = ("name", "value", "verified_at")

    def __init__(self, name: str, value: str, verified_at: Optional[str] = None):
        self.name = name
        self.value = value
        self.verified_at = (
            datetime.fromisoformat(verified_at.replace("Z", "+00:00"))
            if verified_at
            else None
        )


class ImageMetaInfos(DataClass):
    __slots__ = ("width", "height", "size", "aspect")

    def __init__(self, width: int, height: int, size: str, aspect: float):
        self.width = width
        self.height = height
        self.size = size
        self.aspect = aspect


class Focus(DataClass):
    __slots__ = ("x", "y")

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class Meta(DataClass):
    __slots__ = ("focus", "original", "small")

    def __init__(
        self,
        original: Union[Dict[str, Any], ImageMetaInfos],
        small: Union[Dict[str, Any], ImageMetaInfos],
        focus: Optional[Union[Dict[str, float], Focus]] = None,
    ):
        if isinstance(focus, Focus) or focus is None:
            self.focus = focus
        else:
            self.focus = Focus(**focus)

        if isinstance(original, ImageMetaInfos):
            self.original = original
        else:
            self.original = ImageMetaInfos(**original)

        if isinstance(small, ImageMetaInfos):
            self.small = small
        else:
            self.small = ImageMetaInfos(**small)



class Source(DataClass):
    __slots__ = (
        "privacy",
        "sensitive",
        "language",
        "note",
        "fields",
        "follow_requests_count",
    )

    def __init__(
        self,
        privacy: str,
        sensitive: bool,
        language: str,
        note: str,
        fields: List[Union[Dict[str, Any], Field]],
        follow_requests_count: int,
    ):
        self.privacy = privacy
        self.sensitive = sensitive
        self.language = language
        self.note = note
        if len(fields) < 1 or isinstance(fields[0], Field):
            self.fields = fields
        else:
            self.fields = [Field(**element) for element in fields]
        self.follow_requests_count = follow_requests_count


class Role(DataClass):
    __slots__ = ("id", "name", "permissions", "color", "highlighted")

    def __init__(
        self, id: str, name: str, permissions: str, color: str, highlighted: bool
    ):
        self.id = id
        self.name = name
        self.permissions = permissions
        self.color = color
        self.highlighted = highlighted


class Account(DataClass): ...  # ? -> Prevent from undefined error
class Account(DataClass):
    __slots__ = (
        "id",
        "username",
        "acct",
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
        "group",
        "discoverable",
        "noindex",
        "moved",
        "suspended",
        "limited",
        "created_at",
        "last_status_at",
        "statuses_count",
        "followers_count",
        "following_count",
        "attribution_domains",
        "source",
        "role",
        "mute_expires_at",
        "indexable",
        "uri",
        "hide_collections",
    )

    def __init__(
        self,
        id: str,
        username: str,
        acct: str,
        url: str,
        display_name: str,
        note: str,
        avatar: str,
        avatar_static: str,
        header: str,
        header_static: str,
        locked: bool,
        fields: List[Union[Dict[str, Any], Field]],
        emojis: List[Union[Dict[str, Any], Emoji]],
        bot: bool,
        created_at: str,
        statuses_count: int,
        followers_count: int,
        following_count: int,
        last_status_at: Optional[str] = None,
        noindex: Optional[bool] = None,
        moved: Optional[Union[Dict[str, Any], "Account"]] = None,
        suspended: Optional[bool] = None,
        limited: Optional[bool] = None,
        group: Optional[bool] = None,
        discoverable: Optional[bool] = None,
        attribution_domains: Optional[List[str]] = None,
        source: Optional[Union[Dict[str, Any], Source]] = None,
        role: Optional[Union[Dict[str, Any], Role]] = None,
        mute_expires_at: Optional[str] = None,
        indexable: Optional[bool] = None,
        uri: Optional[str] = None,
        hide_collections: Optional[Any] = None,
        roles: Optional[List[Any]] = None,
    ):
        self.id = id
        self.username = username
        self.acct = acct
        self.url = url
        self.display_name = display_name
        self.note = note
        self.avatar = avatar
        self.avatar_static = avatar_static
        self.header = header
        self.header_static = header_static
        self.locked = locked
        if len(fields) < 1 or isinstance(fields[0], Field):
            self.fields = fields
        else:
            self.fields = [Field(**element) for element in fields]
        if len(emojis) < 1 or isinstance(emojis[0], Emoji):
            self.emojis = emojis
        else:
            self.emojis = [Emoji(**element) for element in emojis]
        self.bot = bot
        self.created_at = (
            datetime.fromisoformat(created_at.replace("Z", "+00:00"))
            if created_at
            else None
        )
        self.last_status_at = (
            datetime.fromisoformat(last_status_at.replace("Z", "+00:00"))
            if last_status_at
            else None
        )
        self.statuses_count = statuses_count
        self.followers_count = followers_count
        self.following_count = following_count
        self.noindex = noindex
        if isinstance(moved, Account):
            self.moved = moved
        elif moved:
            self.moved = Account(**moved)
        else:
            self.moved = None
        self.suspended = suspended
        self.limited = limited
        self.group = group
        self.discoverable = discoverable
        self.attribution_domains = attribution_domains
        if isinstance(source, Source):
            self.source = source
        elif source:
            self.source = Source(**source)
        else:
            self.source = None
        if isinstance(role, Role):
            self.role = role
        elif role:
            self.role = Role(**role)
        else:
            self.role = None
        self.mute_expires_at = (
            datetime.fromisoformat(mute_expires_at.replace("Z", "+00:00"))
            if mute_expires_at
            else None
        )
        self.indexable = indexable
        self.uri = uri
        self.hide_collections = hide_collections
        self.roles = roles
        # print(indexable, uri, hide_collections, roles)


class Application(DataClass):
    __slots__ = ("name", "website")

    def __init__(self, name: str, website: Optional[str] = None):
        self.name = name
        self.website = website


class Mention(DataClass):
    __slots__ = ("id", "username", "url", "acct")

    def __init__(self, id: str, username: str, url: str, acct: str):
        self.id = id
        self.username = username
        self.url = url
        self.acct = acct


class Tag(DataClass):
    __slots__ = ("name", "url")

    def __init__(self, name: str, url: str):
        self.name = name
        self.url = url


class MediaAttachment(DataClass):
    __slots__ = (
        "id",
        "type",
        "url",
        "preview_url",
        "remote_url",
        "meta",
        "description",
        "blurhash",
        "preview_remote_url",
        "text_url",
    )

    def __init__(
        self,
        id: str,
        type: str,
        url: str,
        preview_url: str,
        preview_remote_url: str,
        meta: Union[Dict[str, Any], Meta],
        text_url: Optional[str] = None,
        remote_url: Optional[str] = None,
        description: Optional[str] = None,
        blurhash: Optional[str] = None,
    ):
        self.id = id
        self.type = type
        self.url = url
        self.preview_url = preview_url
        self.remote_url = remote_url
        if isinstance(meta, Meta):
            self.meta = meta
        else:
            self.meta = Meta(**meta)
        self.description = description
        self.blurhash = blurhash
        self.preview_remote_url = preview_remote_url
        self.text_url = text_url


class Poll(DataClass):
    __slots__ = (
        "id",
        "expires_at",
        "expired",
        "multiple",
        "votes_count",
        "voters_count",
        "options",
        "emojis",
        "voted",
    )

    def __init__(
        self,
        id: str,
        expires_at: str,
        expired: bool,
        multiple: bool,
        votes_count: int,
        voters_count: int,
        options: List[Dict[str, Any]],
        emojis: List[Union[Dict[str, Any], Emoji]],
        voted: Optional[bool] = None,
    ):
        self.id = id
        self.expires_at = (
            datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
            if expires_at
            else None
        )
        self.expired = expired
        self.multiple = multiple
        self.votes_count = votes_count
        self.voters_count = voters_count
        self.options = options
        if len(emojis) < 1 or isinstance(emojis[0], Emoji):
            self.emojis = emojis
        else:
            self.emojis = [Emoji(**element) for element in emojis]
        self.voted = voted


class PreviewCard(DataClass):
    __slots__ = (
        "url",
        "title",
        "description",
        "type",
        "author_name",
        "author_url",
        "provider_name",
        "provider_url",
        "html",
        "width",
        "height",
        "image",
        "embed_url",
        "blurhash",
    )

    def __init__(
        self,
        url: str,
        title: str,
        description: str,
        type: str,
        author_name: str,
        author_url: str,
        provider_name: str,
        provider_url: str,
        html: str,
        width: int,
        height: int,
        embed_url: str,
        image: Optional[str] = None,
        blurhash: Optional[str] = None,
    ):
        self.url = url
        self.title = title
        self.description = description
        self.type = type
        self.author_name = author_name
        self.author_url = author_url
        self.provider_name = provider_name
        self.provider_url = provider_url
        self.html = html
        self.width = width
        self.height = height
        self.image = image
        self.embed_url = embed_url
        self.blurhash = blurhash


class Status(DataClass):
    __slots__ = (
        "id",
        "uri",
        "created_at",
        "account",
        "content",
        "visibility",
        "sensitive",
        "spoiler_text",
        "media_attachments",
        "application",
        "mentions",
        "tags",
        "emojis",
        "reblogs_count",
        "favourites_count",
        "replies_count",
        "url",
        "in_reply_to_id",
        "in_reply_to_account_id",
        "reblog",
        "poll",
        "card",
        "language",
        "text",
        "edited_at",
        "favourited",
        "reblogged",
        "muted",
        "bookmarked",
        "pinned",
        "filtered",
    )

    def __init__(
        self,
        id: str,
        uri: str,
        created_at: str,
        account: Union[Account, Dict[str, Any]],
        content: str,
        visibility: str,
        sensitive: bool,
        spoiler_text: str,
        media_attachments: List[Union[Dict[str, Any], MediaAttachment]],
        mentions: List[Union[Dict[str, Any], Mention]],
        tags: List[Union[Dict[str, Any], Tag]],
        emojis: List[Union[Dict[str, Any], Emoji]],
        reblogs_count: int,
        favourites_count: int,
        replies_count: int,
        application: Optional[Union[Dict[str, Any], Application]] = None,
        url: Optional[str] = None,
        in_reply_to_id: Optional[str] = None,
        in_reply_to_account_id: Optional[str] = None,
        reblog: Optional["Status"] = None,
        poll: Optional[Union[Dict[str, Any], Poll]] = None,
        card: Optional[Union[Dict[str, Any], PreviewCard]] = None,
        language: Optional[str] = None,
        text: Optional[str] = None,
        edited_at: Optional[str] = None,
        favourited: Optional[bool] = None,
        reblogged: Optional[bool] = None,
        muted: Optional[bool] = None,
        bookmarked: Optional[bool] = None,
        pinned: Optional[bool] = None,
        filtered: Optional[List[Dict[str, Any]]] = None,
    ):
        self.id = id
        self.uri = uri
        self.created_at = (
            datetime.fromisoformat(created_at.replace("Z", "+00:00"))
            if created_at
            else None
        )
        if isinstance(account, Account):
            self.account = account
        else:
            self.account = Account(**account)
        self.content = content
        self.visibility = visibility
        self.sensitive = sensitive
        self.spoiler_text = spoiler_text
        if len(media_attachments) < 1 or isinstance(media_attachments[0], MediaAttachment):
            self.media_attachments = media_attachments
        else:
            self.media_attachments = [
                MediaAttachment(**element) for element in media_attachments
            ]
        if isinstance(application, Application) or poll is None:
            self.application = application
        else:
            self.application = Application(**application)
        if len(mentions) < 1 or isinstance(mentions[0], Mention):
            self.mentions = mentions
        else:
            self.mentions = [Mention(**element) for element in mentions]
        if len(tags) < 1 or isinstance(tags[0], Tag):
            self.tags = tags
        else:
            self.tags = [Tag(**element) for element in tags]
        if len(emojis) < 1 or isinstance(emojis[0], Emoji):
            self.emojis = emojis
        else:
            self.emojis = [Emoji(**element) for element in emojis]
        self.reblogs_count = reblogs_count
        self.favourites_count = favourites_count
        self.replies_count = replies_count
        self.url = url
        self.in_reply_to_id = in_reply_to_id
        self.in_reply_to_account_id = in_reply_to_account_id
        self.reblog = reblog
        if isinstance(poll, Poll) or poll is None:
            self.poll = poll
        else:
            self.poll = Poll(**poll)
        if isinstance(card, PreviewCard) or poll is None:
            self.card = card
        else:
            self.card = PreviewCard(**card)
        self.language = language
        self.text = text
        self.edited_at = (
            datetime.fromisoformat(edited_at.replace("Z", "+00:00"))
            if edited_at
            else None
        )
        self.favourited = favourited
        self.reblogged = reblogged
        self.muted = muted
        self.bookmarked = bookmarked
        self.pinned = pinned
        self.filtered = filtered
