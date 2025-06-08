"""
The client !
"""

from typing import Any, Dict, Callable, IO, Tuple, Optional, Literal

from .Exceptions import *
from .utils import DEBUG, TRY, LOG, get_user_input
from .DataClasses import *

import re
import time

import requests, json
import traceback


TOKEN_FORMAT = re.compile(r"^[A-Za-z0-9\-_]{43}$")
SERVER_FORMAT = re.compile(r"^(http(s)?:\/\/)?([a-zA-Z0-9-]{1,61}\.){1,}[a-zA-Z]{2,}$")


class Client:
    """
    A class representing your application.
    """

    def __init__(
        self, /, token: str, server: str = "https://mastodon.social"
    ) -> None:
        """The representation of your aplication.

        Args:
            token (str): The token to auth requests to the API.
            server (str, optional): The url to the instance where your account is registered. Defaults to "https://mastodon.social".
        """

        if not isinstance(token, str):
            raise TypeError(f"Token type `{type(token)}` not supported must be a str.")
        token = token.strip()
        if len(token) != 43:
            raise ValueError(f"Token lenght must be 43 characters not {len(token)}.")
        if not TOKEN_FORMAT.match(token):
            raise ValueError("Token doesn't match the format.")
        self.token = token

        if not isinstance(server, str):
            raise TypeError(
                f"Server type `{type(server)}` not supported must be a str."
            )
        if not SERVER_FORMAT.match(server):
            raise ValueError("Server url doesn't match the format.")
        if not server.startswith("https://") and not server.startswith("http://"):
            server = "https://" + server
            if not SERVER_FORMAT.match(server):
                raise ValueError("Server url doesn't match the format.")
        self.server = server

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

        self.RUNNING = False

    def __repr__(self) -> str:
        return "Client(token=f'{SECRET_TOKEN}')"

    def stop(self):
        """stop the main mainloop"""
        self.RUNNING = False

    stop.__doc__ = """stop the main mainloop"""  # ? I dont know why if I dont put this line stop.__doc__  is None

    def _step(self, i: Optional[int] = None) -> None:
        if not isinstance(self.epoch, float):
            raise MasthonException("Loop not started, impossible to execute one step.")
        for func, time_after in self.scheduled.items():
            if time.time() - self.epoch >= time_after:
                func(self)
                del self.scheduled[func]
        for loop_time, flist in self.funcs.items():
            for j, (last, func) in enumerate(flist):
                if last - time.time() <= -loop_time:
                    func(self)
                    self.funcs[loop_time][j] = time.time(), func

    def run(self) -> None:
        """Run the mainloop.

        Raises:
            RuntimeError: If you try to run an instance into.
            CommandNotFound: ...
            e.args: Errors that they are raised by your commands.
            CommandExecutionError: Not really raised.
        """
        if self.RUNNING:
            raise RuntimeError("You can't run two instances at the same time.")
        i = 0
        self.RUNNING = True
        self.epoch = time.time()
        while self.RUNNING:
            u_input = get_user_input()
            if u_input:
                try:
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

    # Derpecated (yeah, already) because CLI not implemented
    # // def _run(self):
    # //     if self.RUNNING:
    # //         raise RuntimeError("You can't run two instances at the same time.")
    # //     i = 0
    # //     self.RUNNING = True
    # //     while self.RUNNING:
    # //         yield i, self._step(i)
    # //         i += 1

    # // def __iter__(self):
    # //     for i, return_ in self._run():
    # //         yield i, return_

    @TRY(HTTPError)
    @LOG(True, True, args_max_lenght=64)
    def _raw_request(
        self,
        path: str,
        /,
        method: RequestMethod,
        annonymous: Optional[bool] = False,
        files: Optional[Dict[str, Tuple[str, IO, str]]] = None,
        additional_data: Dict[str, str] = dict(),
        **kwargs: Dict[str, str],
    ) -> requests.Response:
        """Make a request to the API.

        Args:
            path (str): The API path.
            method (some http method): The http method used
            annonymous (bool, optional): If True, token is omitten. Defaults to False.
            files (str, optional): Files to post. Defaults to None.
            additional_data (dict, optional): Data to add that you can put as a kwarg (like `"media_ids[]"`). Defaults to dict().

        Raises:
            HTTPError: If status_code not 2xx or 3xx.

        Returns:
            requests.Response: The response from the API.
        """
        url = self.server + path
        auth = {"Authorization": f"Bearer {self.token}"} if not annonymous else dict()
        data = {**kwargs, **additional_data}

        match method:
            case RequestMethod.GET:
                response = requests.get(url, data=kwargs, headers=auth, files=files)
            case RequestMethod.POST:
                response = requests.post(url, data=kwargs, headers=auth, files=files)
            case RequestMethod.DELETE:
                response = requests.delete(url, data=kwargs, headers=auth, files=files)
            case RequestMethod.PUT:
                response = requests.put(url, data=kwargs, headers=auth, files=files)
            case RequestMethod.PATCH:
                response = requests.patch(url, data=kwargs, headers=auth, files=files)
            case _:
                raise HTTPError(f"Method `{method}` not known")

        if response.status_code == 429:
            self.stop()
            raise HTTP401Error("429 Too many requests: Slow down !")

        match response.status_code // 100:
            case 4:
                if response.status_code == 401:
                    raise HTTP401Error("401 Unauthorized: Your acces token is invalid")
                raise HTTPRequestError400(
                    f"The request is invalid : HTTP Error {response.status_code}",
                    "\n",
                    json.loads(response.text)["error"],
                )
            case 5:
                raise HTTPServerError500(
                    f"An error as occured from the server `{self.server}` : HTTP Error {response.status_code}",
                    "\n",
                    json.loads(response.text)["error"],
                )
            case _:
                pass
        return response

    @LOG()
    def post_status(
        self,
        text: str = "Hello World from Mastodon API !",
        medias: Optional[List[str]] = [],
        visibility: Visibility = Visibility.UNLISTED,  # ? Changed to unlisted to prevent spam
        in_reply_to_id: Optional[str] = None,
        sensitive: Optional[Literal[None, True]] = None,
        language: Optional[str] = "en",
    ) -> Status:
        """Post a status.

        Args:
            text (str, optional): The message to send. Defaults to "Hello World from Mastodon API !".
            medias (List[str], optional): A list of media's ids to link with the status. Defaults to [].
            visibility (Visibility, optional): ... Defaults to "unlisted".
            in_reply_to_id (str, optional): If post reply to another, put his id here. Defaults to None.
            sensitive (NoneType | True, optional): True to make; None to dont. False is making the post sensitive. Defaults to None.
            language (str, optional): ISO 639 language code for this status. Defaults to "en".

        Returns:
            Status: This status as an object.
        """
        ids = list()
        if isinstance(medias, list):
            for media_src in medias:
                ids.append(str(self.upload_media(media_src).id))
        response = self._raw_request(
            "/api/v1/statuses",
            method=RequestMethod.POST,
            status=text,
            visibility=visibility.value,
            additional_data={"media_ids[]": ids},
            in_reply_to_id=in_reply_to_id,
            sensitive=sensitive,
            language=language,
        )
        return Status(**json.loads(response.text))

    @LOG()
    def upload_media(
        self, src: str, /, type_: str = "image/{ext}"
    ) -> MediaAttachment:
        """Upload a media (syncronously) with /api/v1

        Args:
            src (str): source of your media file
            type_ (str, optional): Like `image/png` but you can formate this with {ext} = after the dot. Defaults to "image/{ext}".

        Returns:
            MediaAttachment: The media uploaded as an object.
        """
        with open(src, "rb") as f:
            files = {
                "file": (src.split("/")[-1], f, type_.format(ext=src.split(".")[-1]))
            }

            response = self._raw_request(
                "/api/v1/media",
                method=RequestMethod.POST,
                files=files,
                data={
                    "description": "Media uploaded with Masthon. @gator3000@mastodon.social for more infos"
                },
            )

        attachement = MediaAttachment(**json.loads(response.text))
        assert attachement.type != "unknown", UnexpectedServerResult()
        return attachement

    @LOG()
    def delete_status(self, status: Status | str, **kwargs) -> requests.Response:
        """Delete given status

        Args:
            status (Status | str): ...

        Returns:
            requests.Response: The response returned by the API.
        """
        if isinstance(status, Status):
            id_ = status.id
        else:
            id_ = status
        response = self._raw_request(
            f"/api/v1/statuses/{id_}", method=RequestMethod.DELETE, **kwargs
        )
        return response

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

    def cli_last(self):
        """display or raise last error raised by a command"""
        if isinstance(self.cli_last_error, Exception):
            if DEBUG:
                raise RealException(self.cli_last_error) from self.cli_last_error
            else:
                traceback.print_exception(self.cli_last_error)

    # Decorators !
    def looped_every(self, time: float = 60) -> Callable:
        """Decorator for loop your own function into the mainloop.

        Args:
            time (float, optional): Every this time your func wil be called. Defaults to 60.

        Returns:
            Callable: ...
        """

        def _decorator(func: Callable) -> Callable:
            if self.funcs.get(time) is None:
                self.funcs[time] = list()

            self.funcs[time].append((0, func))  # (last time executed, function)

            return func

        return _decorator

    def schedule(self, after: float = 0) -> Callable:
        """Shedule your func x time after it being runned.

        Args:
            after (float, optional): ... Defaults to 0.

        Returns:
            Callable: ...
        """

        def _decorator(func: Callable) -> Callable:
            self.scheduled[func] = after

            return func

        return _decorator

    def add_command(self, name: str) -> Callable:
        """Add your own command to the cli system.

        Args:
            name (str): The name to call it.

        Returns:
            Callable: ...
        """

        def _decorator(func: Callable) -> Callable:
            self.commands[name] = func

            return func

        return _decorator
