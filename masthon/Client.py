from typing import Any, Dict, Callable

from .Exceptions import *
from .utils import TRY, LOG, get_user_input

import re
import requests
import time



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

        self.funcs = {}

        self.commands = {"stop": Client.stop, "help": Client.CLI_help, "h": Client.CLI_help, "last": Client.cli_last}
        self.cli_last_error = None

        self.RUNNING = False

    def __repr__(self) -> str:
        return "Client(token=f'{SECRET_TOKEN}')"

    @LOG(True, False)
    def stop(self):
        """stop the main mainloop"""
        self.RUNNING = False
    stop.__doc__ = """stop the main mainloop"""

    @TRY
    def _step(self, i: int = None) -> None:
        for loop_time, flist in self.funcs.items():
            for j, (last, func) in enumerate(flist):
                if last - time.time() < -loop_time:
                    func(self)
                    self.funcs[loop_time][j] = time.time(), func


    def run(self) -> None:
        if self.RUNNING:
            raise RuntimeError("You can't run two instances at the same time.")
        i = 0
        self.RUNNING = True
        while self.RUNNING:
            u_input = get_user_input()
            if u_input:
                try:
                    cmd, *cmdargs = u_input.split(" ")
                    if cmd not in self.commands:
                        raise CommandNotFound(f"Command `{cmd}` not found. Type help to see commands that you can use `help` or `h`.")
                    try:
                        self.commands[cmd](self, *cmdargs)
                    except Exception as e:
                        self.cli_last_error = e
                        print(e)
                        raise CommandExecutionError(f"An exception as occured while executing the command named {cmd}.")
                except CLIException as e:
                    print(f"\033[91m\033[1m{e.__class__.__name__}: \033[0m\033[91m{repr(e)}\033[0m")
            self._step(i)
            i += 1

    def _run(self):
        if self.RUNNING:
            raise RuntimeError("You can't run two instances at the same time.")
        i = 0
        self.RUNNING = True
        while self.RUNNING:
            yield i, self._step(i)
            i += 1

    def __iter__(self):
        for i, return_ in self._run():
            yield i, return_

    @LOG(True, False)
    def _raw_request_post(
        self, path: str, /, annonymous: bool = False, **kwargs: Dict[str, str]
    ) -> requests.Response:
        url = self.server + path
        auth = {"Authorization": f"Bearer {self.token}"} if not annonymous else dict()
        response = requests.post(url, data=kwargs, headers=auth)

        if response.status_code == 429:
            self.stop()

        return response

    def post_status(self, text="Hello World from Mastodon API !") -> requests.Response:
        return self._raw_request_post("/api/v1/statuses", status=text)

    def looped_every(self, time: float = 60) -> Callable:
        def _decorator(func: Callable) -> Callable:
            if self.funcs.get(time) is None:
                self.funcs[time] = list()

            self.funcs[time].append((0, func))  # (last time executed, function)

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
 - """ + "\n - ".join(self.commands.keys()) + "\033[0m"
            )
        else:
            if self.commands.get(command) is None:
                raise CommandNotFound()
            print(f"\033[1m{command} - \033[0m{self.commands[command].__doc__}")
    
    def cli_last(self):
        print(self.cli_last_error)