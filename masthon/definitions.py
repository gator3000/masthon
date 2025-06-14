from typing import *
from abc import abstractmethod

from .DataClasses import *
from .Exceptions import *
from .utils import *

import requests


class Client:
    @abstractmethod
    def __init__(
        self,
        token: str,
        server: str = "https://mastodon.social",
        *,
        used_events: Optional[Event | Tuple[Event]] = None,
        event_reactivity: int = 15,
    ) -> None: ...

    @abstractmethod
    def stop(self) -> None: ...

    @abstractmethod
    def _step(self, i: Optional[int] = None) -> None: ...

    @abstractmethod
    def run(self) -> None: ...

    @abstractmethod
    def _raw_request(
        self,
        path: str,
        /,
        method: RequestMethod,
        annonymous: Optional[bool] = False,
        files: Optional[Dict[str, Tuple[str, IO, str]]] = None,
        additional_data: Dict[str, str] = dict(),
        ratelimit_security: bool = True,
        **kwargs: Dict[str, str],
    ) -> requests.Response: ...

    @abstractmethod
    def post_status(
        self,
        text: str = "Hello World from Mastodon API !",
        medias: Optional[List[str]] = [],
        visibility: Visibility = Visibility.UNLISTED,
        in_reply_to_id: Optional[str] = None,
        sensitive: Optional[Literal[None, True]] = None,
        language: Optional[str] = "en",
        **kwargs,
    ) -> Status: ...

    @abstractmethod
    def upload_media(
        self, src: str, *, type_: str = "image/{ext}", **kwargs
    ) -> MediaAttachment: ...

    @abstractmethod
    def delete_status(self, status: Status | str, **kwargs) -> requests.Response: ...

    @abstractmethod
    def unread_notifications_count(
        self, types: Iterable[NotificationType] = [], **kwargs
    ) -> int: ...

    @abstractmethod
    def get_notifications(
        self, limit: Optional[int] = None, **kwargs
    ) -> List[Notification]: ...

    @abstractmethod
    def get_marker(
        self, timeline: Iterable[TimelineType], **kwargs
    ) -> Dict[TimelineType, Marker]: ...

    @abstractmethod
    def post_marker(
        self, timelines: Dict[TimelineType, str], **kwargs
    ) -> Dict[TimelineType, Marker]: ...

    @abstractmethod
    def CLI_help(self, command: Optional[str] = None) -> None: ...

    @abstractmethod
    def CLI_short_help(self) -> None: ...

    @abstractmethod
    def cli_last(self) -> None: ...

    @abstractmethod
    def looped_every(self, time: float = 60) -> Callable: ...

    @abstractmethod
    def schedule(self, after: float = 0) -> Callable: ...

    @abstractmethod
    def add_command(self, name: str) -> Callable: ...

    @abstractmethod
    def listen_for(self, event: Event) -> Callable: ...
