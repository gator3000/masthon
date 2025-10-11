"""
The client !
"""

from typing import Any, Dict, Callable, IO, Tuple, Optional, Literal, Set, Iterable

import threading as tg

from .Exceptions import *
from .utils import *
from .DataClasses import *
from .Events import Listeners

import re
import time

import requests, json
import traceback


TOKEN_FORMAT: re.Pattern = re.compile(r"^[A-Za-z0-9\-_]{43}$")
SERVER_FORMAT: re.Pattern = re.compile(
    r"^(http(s)?:\/\/)?([a-zA-Z0-9-]{1,61}\.){1,}[a-zA-Z]{2,}$"
)
# SERVER_FORMAT: re.Pattern = re.compile( r"^https?://([a-zA-Z0-9-]{1,61}\.)+[a-zA-Z]{2,}(/api/v[0-9]+)?/?$") #pour ajouter api/v1
apiversion1 = "/api/v1"
apiversion2 = "/api/v2"


class Client:
    """
    The representation of your app

    __init__:

    Parameters
    ----------
    token : str
        the token of it (must be 43 chars)
    server : str, optional
        a link to your instance, by default "https://mastodon.social"
    async_level : int, optional
        The level of using threading, by default 0
    used_events : Optional[Event  |  Tuple[Event]], optional
        A tuple of events you will wait (else they will be never be run), by default None
    event_reactivity : int, optional
        Every x seconds events will be checked if they must be run, by default 15 (sec)
    """

    def __init__(
        self,
        token: str,
        server: str = "https://mastodon.social",
        *,
        async_level: int = 0,
        used_events: Optional[Event | Tuple[Event]] = None,
        event_reactivity: int = 15,
    ) -> None:
        """
        The representation of your app

        Parameters
        ----------
        token : str
            the token of it (must be 43 chars)
        server : str, optional
            a link to your instance, by default "https://mastodon.social"
        async_level : int, optional
            The level of using threading, by default 0
        used_events : Optional[Event  |  Tuple[Event]], optional
            A tuple of events you will wait (else they will be never be run), by default None
        event_reactivity : int, optional
            Every x seconds events will be checked if they must be run, by default 15 (sec)
        """

        # token format checker
        if not isinstance(token, str):
            raise TypeError(f"Token type `{type(token)}` not supported must be a str.")
        token = token.strip()
        if len(token) != 43:
            raise ValueError(f"Token lenght must be 43 characters not {len(token)}.")
        if not TOKEN_FORMAT.match(token):
            raise ValueError("Token doesn't match the format.")
        self.token = token

        # server format checker
        if not isinstance(server, str):
            raise TypeError(
                f"Server type `{type(server)}` not supported must be a str."
            )
        if not SERVER_FORMAT.match(
            server
        ):  # changer pour adapter a https://vzhbh/api/v1
            raise ValueError("Server url doesn't match the format.")
        if not server.startswith("https://") and not server.startswith("http://"):
            server = "https://" + server
            if not SERVER_FORMAT.match(server):
                raise ValueError("Server url doesn't match the format.")
        self.server = server

        self.listeners = Listeners(self)
        self.activated_listeners: Dict[Event, List[Callable]]
        if used_events is None:
            self.activated_listeners = dict()
        else:
            if isinstance(used_events, tuple):
                self.activated_listeners = {
                    event: list() for event in Event if event in used_events
                }
            elif isinstance(used_events, Event):
                self.activated_listeners = {
                    event: list() for event in Event if used_events == event
                }
            else:
                raise TypeError("Events type not handeled.")

        self.event_reactivity: int = (
            event_reactivity if len(self.activated_listeners) else -1
        )
        self.last_listened: float = -self.event_reactivity

        self.epoch: Optional[float] = None
        self.funcs: Dict[float, List[Tuple[float, Callable]]] = {}
        self.scheduled: Dict[Callable, float] = {}

        self.commands: Dict[str, Callable] = {
            "stop": Client.stop,
            "help": Client.CLI_help,
            "h": Client.CLI_short_help,
            "last": Client.cli_last,
        }
        self.cli_last_error: Optional[Exception] = None

        if not (0 <= async_level <= 2):
            print(
                "\033[1m\033[91m[WARN]\033[93m Async level unknown >\033[0m default set to 0"
            )
            async_level = 0
        self._async_level = async_level

        self.process: List[tg.Thread] = list()

        self.RUNNING = False

    def __repr__(self) -> str:
        return "Client(token=f'{SECRET_TOKEN}'" + f", server='{self.server}')"

    def __format__(self, modifier: Optional[str] = None) -> str:
        if modifier is not None and modifier.upper() == "DISPLAY_TOKEN":
            return repr(self).format(SECRET_TOKEN=self.token)
        else:
            return repr(self)

    def stop(self) -> None:
        """stop the main mainloop"""
        self.RUNNING = False

    stop.__doc__ = """stop the main mainloop"""  # ? I dont know why if I dont put this line stop.__doc__  is None

    def _step(self, i: int) -> None:
        # Checks
        if not isinstance(self.epoch, float):
            raise MasthonException("Loop not started, impossible to execute one step.")

        # Calling
        self._on_loop_step_(self, i)

        # process list initialisation
        match self._async_level:
            case 0:
                pass  # not used
            case 1:
                self.process.clear()  # cleared because all process down
            case 2:
                for i, p in enumerate(self.process):
                    if not p.is_alive():
                        del self.process[
                            i
                        ]  # juste delete process down and let other run
        self.process = list()

        # Sheduled functions (executed one time)
        executed = list()
        for func, time_after in self.scheduled.items():
            if time.time() - self.epoch >= time_after:
                match self._async_level:
                    case 0:
                        func(self)
                    case 1:
                        self.process.append(tg.Thread(target=func, args=(self,)))
                        self.process[-1].start()
                    case 2:
                        self.process.append(tg.Thread(target=func, args=(self,)))
                        self.process[-1].start()
                executed.append(func)
        for f in executed:
            del self.scheduled[f]

        # Looped functions (every `loop_time`)
        for loop_time, flist in self.funcs.items():
            for j, (last, func) in enumerate(flist):
                if last - time.time() <= -loop_time:
                    match self._async_level:
                        case 0:
                            func(self)
                        case 1:
                            self.process.append(tg.Thread(target=func, args=(self,)))
                            self.process[-1].start()
                        case 2:
                            self.process.append(tg.Thread(target=func, args=(self,)))
                            self.process[-1].start()
                    self.funcs[loop_time][j] = time.time(), func

        # Event handling
        if (
            self.event_reactivity > 0
            and time.time() - self.last_listened >= self.event_reactivity
        ):
            match self._async_level:
                case 0:
                    self._event_handling()
                case 1:
                    self.process.append(tg.Thread(target=self._event_handling))
                    self.process[-1].start()
                case 2:
                    self.process.append(tg.Thread(target=self._event_handling))
                    self.process[-1].start()

        # End
        match self._async_level:
            case 0:
                pass
            case 1:
                # Join all process
                for p in self.process:
                    p.join()
            case 2:
                pass

    def _event_handling(self) -> None:
        self.last_listened = time.time()
        for event, funcs in self.activated_listeners.items():
            #! Not async but whole method is, and we need results before continuing
            out = self.listeners.listen_for(event)
            if out.status == EventStatus.TRIGGERED:
                for func in funcs:
                    match self._async_level:
                        case 0:
                            func(self, out.data)
                        case 1:
                            self.process.append(
                                tg.Thread(target=func, args=(self, out.data))
                            )
                            self.process[-1].start()
                        case 2:
                            self.process.append(
                                tg.Thread(target=func, args=(self, out.data))
                            )
                            self.process[-1].start()

    def run(self) -> None:
        """Run the mainloop.

        Raises:
            RuntimeError: If you try to run an instance into another.
        """
        if self.RUNNING:
            raise RuntimeError("You can't run two instances at the same time.")
        i = 0
        self.RUNNING = True
        self.epoch = time.time()

        self._on_start_(self)

        try:
            while self.RUNNING:
                u_input = get_user_input()
                if u_input:
                    try:
                        # Get command from inputed string
                        cmd, *cmdargs = u_input.split(" ")
                        if cmd not in self.commands:
                            raise CommandNotFound(
                                f"Command `{cmd}` not found. Type help to see commands that you can use `help` or `h`."
                            )
                        try:
                            self.commands[cmd](self, *cmdargs)
                        except Exception as e:
                            self.cli_last_error = e
                            if isinstance(e, RealException):
                                raise e.args[0] from e.args[0]
                            raise CommandExecutionError(
                                f"An exception as occured while executing the command named `{cmd}`.",
                                e,
                            )
                    except CLIException as e:
                        print(
                            f"\033[91m\033[1m{e.__class__.__name__}: \033[0m\033[91m{e.args[0]}\033[0m"
                        )
                self._step(i)
                i += 1
        finally:
            self._on_stop_(self)
            self.RUNNING = False

    @TRY(HTTPError)
    @LOG(True, True)
    def _raw_request(
        self,
        path: str,
        method: RequestMethod,
        annonymous: Optional[bool] = False,
        files: Optional[Dict[str, Tuple[str, IO, str]]] = None,
        additional_data: Dict[str, str] = {},
        json_data: bool = False,
        ratelimit_security: bool = True,
        **kwargs: Dict[str, str],
    ) -> requests.Response:
        """
        Make a call to the API at `self.server`

        Parameters
        ----------
        path : str
            The API path requested
        method : RequestMethod
            some http methode
        annonymous : Optional[bool], optional
            I true, token will not be provided to the API (may result in HTTPError400), by default False
        files : Optional[Dict[str, Tuple[str, IO, str]]], optional
            Files to transfer, by default None
        additional_data : Dict[str, str], optional
            ..., by default {}
        json_data : bool, optional
            Send data as json if true, by default False
        ratelimit_security : bool, optional
            Stop the loop if server raise HTTPRateLimit, by default True

        Returns
        -------
        requests.Response
            The server's response.

        Raises
        ------
        HTTPRateLimit
            ...
        HTTP401Error
            ...
        HTTPRequestError400
            ...
        HTTPServerError500
            ...
        """
        url = self.server + path
        # print(url)
        auth = {"Authorization": f"Bearer {self.token}"} if not annonymous else dict()
        data = {**kwargs, **additional_data}
        args = {"json": data} if json_data else {"data": data}

        if not json_data:
            response = requests.request(
                method.value.upper(), url, headers=auth, files=files, data=data
            )
        else:
            response = requests.request(
                method.value.upper(), url, headers=auth, files=files, json=data
            )
        self.check_statuscode(response, ratelimit_security)

        return response

    def check_statuscode(self, response, ratelimit_security: bool = True):
        try:
            error_msg = response.json().get("error", "Unknown error")
        except ValueError:
            error_msg = "Response body is not valid JSON"

        match response.status_code // 100:
            case 4:
                if response.status_code == 401:
                    raise HTTP401Error(
                        "401 Unauthorized: Your access token is invalid",
                        response.status_code,
                    )
                elif response.status_code == 429:
                    if ratelimit_security:
                        self.stop()
                    raise HTTPRateLimit("429 Too many requests: Slow down!")
                else:
                    raise HTTPRequestError400(
                        f"The request is invalid : HTTP Error {response.status_code}",
                        error_msg,
                        response.status_code,
                    )
            case 5:
                raise HTTPServerError500(
                    f"An error as occurred from the server `{self.server}` : HTTP Error {response.status_code}",
                    response.status_code,
                )
            case _:
                pass  # a changer pour et ajouter case pour erreur type 300 (redirection),200(success),100(informationnel)

    @LOG()
    def post_status(
        self,
        text: str,  # ? default value deleted : pretty useless
        medias: Optional[List[str]] = [],
        visibility: Visibility = Visibility.UNLISTED,  # ? Changed to unlisted to prevent spam
        in_reply_to_id: Optional[str] = None,
        sensitive: Optional[Literal[None, True]] = None,
        language: Optional[str] = "en",
        **kwargs,
    ) -> List[Status] | Status:
        """
        Post a status.

        Parameters
        ----------
        text : str
            The raw text to send.
        medias: Optional[List[str]]
            Pathes to medias to uploads and attach to the post, by default []
        visibility : Visibility, optional
            ... of the status, by default Visibility.UNLISTED
        in_reply_to_id: Optional[str]
            ID of a status (post will reply to it), by default None
        sensitive : Optional[Literal[None, True]], optional
            Mark post as sensitive or not, by default None
        language : Optional[str], optional
            ISO 639 language code for this status, by default "en"

        Returns
        -------
        List[Status] | Status
            Status(es) returned (most time a single)
        """
        ids = list()
        if isinstance(medias, list):
            for media_src in medias:
                ids.append(str(self.upload_media(media_src).id))

        response = self._raw_request(
            path=f"{apiversion1}/statuses",
            method=RequestMethod.POST,
            status=text,
            visibility=visibility.value,
            additional_data={"media_ids[]": ids},
            in_reply_to_id=in_reply_to_id,
            sensitive=sensitive,
            language=language,
            **kwargs,
        )
        # print(response)
        if isinstance(response.json(), list):
            return [Status(**el) for el in response.json()]
        else:
            return Status(**response.json())

    @LOG()
    def upload_media(
        self, src: str, *, type_: MediaType = MediaType.IMAGE, **kwargs
    ) -> MediaAttachment:
        """
        Upload a media (syncronously) with /api/v1

        Parameters
        ----------
        src : str
            source (path) of media to upload
        type_ : MediaType, optional
            The type of the media, by default MediaType.IMAGE

        Returns
        -------
        MediaAttachment
            The media uploaded as an object.
        """
        with open(src, "rb") as f:
            files = {"file": (src.split("/")[-1], f, type_.value)}

            response = self._raw_request(
                path=f"{apiversion1}/media",
                method=RequestMethod.POST,
                files=files,
                data={
                    "description": "Media uploaded with Masthon. @gator3000@mastodon.social for more infos"
                },
                **kwargs,
            )

        attachement = MediaAttachment(**response.json())
        assert attachement.type != "unknown", UnexpectedServerResult()
        return attachement

    @LOG()
    def delete_status(self, status: Status | str, **kwargs) -> requests.Response:
        """
        Delete given Status.

        Parameters
        ----------
        status : Status | str
            The status to delete, or it's id

        Returns
        -------
        requests.Response
            ...
        """
        if isinstance(status, Status):
            id_ = status.id
        else:
            id_ = status
        response = self._raw_request(
            path=f"{apiversion1}/statuses/{id_}",
            method=RequestMethod.DELETE,
            ratelimit_security=False,
            **kwargs,
        )
        return response

    @LOG()
    def unread_notifications_count(
        self, types: Iterable[NotificationType] = [], **kwargs
    ) -> int:
        """
        Args:
            types (List[NotificationType], optinal): types counted

        Returns:
            int: ...
        """
        response = self._raw_request(
            path=add_url_parameters(
                f"{apiversion1}/notifications/unread_count", types=types, **kwargs
            ),
            method=RequestMethod.GET,
        )
        return int(response.json()["count"])

    @LOG()
    def get_notifications(
        self,
        types: Iterable[NotificationType] = [],
        limit: Optional[int] = None,
        min_id: Optional[str] = None,
        **kwargs,
    ) -> List[Notification]:
        """
        Gets you notifications feed

        Parameters
        ----------
        types : Iterable[NotificationType], optional
            Types returned, by default []
        limit : Optional[int], optional
            ..., by default None
        min_id : Optional[str], optional
            Returns only newer than this id, by default None

        Returns
        -------
        List[Notification]
            ...
        """
        response = self._raw_request(
            path=add_url_parameters(
                f"{apiversion1}/notifications",
                limit=limit,
                types=types,
                min_id=min_id,
                **kwargs,
            ),
            method=RequestMethod.GET,
        )
        return [Notification(**el) for el in response.json()]

    @LOG()
    def get_marker(
        self, timeline: Iterable[TimelineType], **kwargs
    ) -> Dict[Type[TimelineType], Marker]:
        """
        Gets the last marker generated of given timelines

        Parameters
        ----------
        timeline : Iterable[TimelineType]
            ...

        Returns
        -------
        Dict[Type[TimelineType], Marker]
            ...
        """
        response = self._raw_request(
            path=add_url_parameters(
                f"{apiversion1}/markers", timeline=[t.value for t in timeline], **kwargs
            ),
            method=RequestMethod.GET,
            **kwargs,
        )
        return {
            convert_to_enum(t, TimelineType): Marker(**el)
            for t, el in response.json().items()
        }

    @LOG()
    def post_marker(
        self, timelines: Dict[str, Dict[str, str]], **kwargs
    ) -> Dict[Type[TimelineType], Marker]:
        """
        Post and generate markers to given ids

        Parameters
        ----------
        timelines : Dict[str, Dict[str, str]]
            Example: `{TimelineType.NOTIFICATIONS.value: {"last_read_id": notification.id}}`

        Returns
        -------
        Dict[Type[TimelineType], Marker]
            markers generated
        """
        response = self._raw_request(
            path=f"{apiversion1}/markers",
            method=RequestMethod.POST,
            additional_data=timelines,
            json_data=True,
            **kwargs,
        )
        return {
            convert_to_enum(t, TimelineType): Marker(**el)
            for t, el in response.json().items()
        }

    # Commands
    def CLI_help(self, command: Optional[str] = None) -> None:
        """display help message"""
        if command is None:
            print(
                """
\033[1mHELP\033[0m:
Commands follow this simple syntax:
    \033[2mcmd arg1_as_str arg2_as_str\033[0m

You can add a command with this code:
\033[2m```py
c = Client(token="")
@c.add_command(name="foo")
def foo_command(client: Client, arg1: str, arg2: str = None):
    print("hello world")

c.run()
```\033[0m

\033[93mAll commands you can use here:
 - """
                + "\n - ".join(self.commands.keys())
                + "\033[0m"
            )
        else:
            if self.commands.get(command) is None:
                raise CommandNotFound()
            print(f"\033[1m{command} - \033[0m{self.commands[command].__doc__}")

    def CLI_short_help(self) -> None:
        """display commands availables"""
        print(
            """
\033[93mAll commands you can use here:
 - """
            + "\n - ".join(self.commands.keys())
            + "\033[0m"
        )

    def cli_last(self) -> None:
        """display or raise last error raised by a command"""
        if isinstance(self.cli_last_error, Exception):
            if DEBUG:
                raise RealException(self.cli_last_error) from self.cli_last_error
            else:
                traceback.print_exception(self.cli_last_error)

    # Decorators !
    def looped_every(self, time: float = 60) -> Callable:
        """
        Decorator generator for loop your own function into the mainloop.

        Parameters
        ----------
        time : float, optional
            Every this time (in seconds) your func wil be called, by default 60 (sec)

        Returns
        -------
        Callable
            Decorator generated
        """

        def _decorator(func: Callable) -> Callable:
            if self.funcs.get(time) is None:
                self.funcs[time] = list()

            self.funcs[time].append((0, func))  # (last time executed, function)

            return func

        return _decorator

    def schedule(self, after: float = 0) -> Callable:
        """
        Decorator generator that shedule your func x seconds after it being runned.

        Parameters
        ----------
        after : float, optional
            In seconds, by default 0 (sec)

        Returns
        -------
        Callable
            Decorator generated
        """

        def _decorator(func: Callable) -> Callable:
            self.scheduled[func] = after

            return func

        return _decorator

    def add_command(self, name: str) -> Callable:
        """
        Add your own command to the cli system.

        Parameters
        ----------
        name : str
            The name to call it

        Returns
        -------
        Callable
            Decorator generated
        """

        def _decorator(func: Callable) -> Callable:
            self.commands[name] = func

            return func

        return _decorator

    def listen_for(self, event: Event) -> Callable:
        """
        Listen for an event and start the function if it come

        Parameters
        ----------
        event : Event
            The event witch will call it

        Returns
        -------
        Callable
            Decorator generated

        Raises
        ------
        EventNotActivated
            Raised if event is not activated at initialisation
        """

        if self.activated_listeners.get(event) is None:
            raise EventNotActivated(
                "You must explicitly activate events that you will use at the creation of your Client"
            )

        def _decorator(func: Callable) -> Callable:
            self.activated_listeners[event].append(func)

            return func

        return _decorator

    def _on_start_(_, self) -> None: ...
    def _on_loop_step_(_, self, i: int) -> None: ...
    def _on_stop_(_, self) -> None: ...

    # def _on_request_(_, self, *args, **kwargs) -> Any: ...

    def execute(self, func: Callable) -> Callable:
        """
        Execute the following function when func.__name__

        Parameters
        ----------
        func : Callable
            func.__name__ has to be formatted

        Returns
        -------
        Callable
            ...

        Raises
        ------
        AttributeError
            If you name your function after an unkwnown simple event
        """

        e_name = "_" + func.__name__ + "_"

        if getattr(self, e_name, None) is None or e_name not in (
            "_on_start_",
            "_on_loop_step_",
            "_on_stop_",
        ):
            raise AttributeError("Event not known.")
        setattr(self, e_name, func)

        return func

    # * Maybe one day it will be possible to modify reqests before they will be sent
    # def __request_modifier__(func: Callable) -> Callable:
    #     def _wrapper(*args, **kwargs) -> Any:
    #         return func(**args, **kwargs)

    #     return _wrapper
