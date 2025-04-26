from typing import Any, Dict, Callable, IO, Tuple, Optional, Literal

from .Exceptions import *
from .utils import TRY, LOG, get_user_input
from .DataClasses import *

import re
import time

import requests, json


TOKEN_FORMAT = re.compile(r"^[A-Za-z0-9\-_]{43}$")
SERVER_FORMAT = re.compile(r"^(http(s)?:\/\/)?([a-zA-Z0-9-]{1,61}\.){1,}[a-zA-Z]{2,}$")


class Client:
    def __init__(self, /, token: str, server: str = "https://mastodon.social") -> None:
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

        self.epoch = None
        self.funcs: Dict[float, List(Tuple[float, Callable])] = {}
        self.scheduled: Dict[Callable, float] = {}

        self.commands = {
            "stop": Client.stop,
            "help": Client.CLI_help,
            "h": Client.CLI_help,
            "last": Client.cli_last,
        }
        self.cli_last_error = None

        self.RUNNING = False

    def __repr__(self) -> str:
        return "Client(token=f'{SECRET_TOKEN}')"

    def stop(self):
        """stop the main mainloop"""
        self.RUNNING = False

    stop.__doc__ = """stop the main mainloop"""

    @TRY
    def _step(self, i: int = None) -> None:
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

    @LOG(True, True)
    def _raw_request_post(
        self,
        path: str,
        /,
        annonymous: bool = False,
        files: Optional[Dict[str, Tuple[str, IO, str]]] = None,
        additional_data: Optional[Dict[str, str]] = {},
        **kwargs: Optional[Dict[str, str]],
    ) -> requests.Response:
        url = self.server + path
        auth = {"Authorization": f"Bearer {self.token}"} if not annonymous else dict()
        response = requests.post(url, data=kwargs, headers=auth, files=files)

        if response.status_code == 429:
            self.stop()

        match response.status_code // 100:
            case 4:
                raise HTTPRequestError400
            case 5:
                raise HTTPServerError500
            case _:
                pass

        return response

    @LOG()
    def post_status(
        self,
        text: str = "Hello World from Mastodon API !",
        medias: Optional[List[str]] = [],
        visibility: Optional[Literal["public", "unlisted", "private", "direct"]] = "public",
    ) -> Status:
        ids = list()
        for media_src in medias:
            ids.append(str(self.upload_media(media_src).id))
        print(ids)
        response = self._raw_request_post(
            "/api/v1/statuses",
            status=text,
            visibility=visibility,
            additional_data={"media_ids[]": ids},
        )
        return Status(**json.loads(response.text))

    @LOG()
    def upload_media(self, src: str) -> MediaAttachment:
        with open(src, "rb") as f:
            files = {"file": (src.split("/")[-1], f, f"image/{src.split('.')[-1]}")}
            response = self._raw_request_post(
                "/api/v1/media",
                files=files,
                data={
                    "description": "Media uploaded with Masthon. @gator3000@mastodon.social for more infos"
                },
            )

        attachement = MediaAttachment(**json.loads(response.text))
        assert attachement.type != "unknown", UnexpectedServerResult()
        return attachement

    def looped_every(self, time: float = 60) -> Callable:
        def _decorator(func: Callable) -> Callable:
            if self.funcs.get(time) is None:
                self.funcs[time] = list()

            self.funcs[time].append((0, func))  # (last time executed, function)

            return func

        return _decorator

    def schedule(self, after: float = 0) -> Callable:
        def _decorator(func: Callable) -> Callable:
            self.scheduled[func] = after

            return func

        return _decorator

    def add_command(self, name: str) -> Callable:
        def _decorator(func: Callable) -> Callable:
            self.commands[name] = func

            return func

        return _decorator

    def CLI_help(self, command: str = None) -> None:
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

    def cli_last(self):
        print(self.cli_last_error.__class__.__name__, ":", self.cli_last_error)
        if self.cli_last_error is not None:
            raise RealException(self.cli_last_error)
