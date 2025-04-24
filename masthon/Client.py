from typing import Any, Dict, Callable

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
        self.RUNNING = False

    def __repr__(self) -> str:
        return f"Client(token='{self.token[:7] + '*'*(20-7) + self.token[20:]}')"

    def stop(self) -> None:
        self.RUNNING = False

    def _step(self, i: int = None) -> Any:
        for loop_time, flist in self.funcs.items:
            for last, func in flist:
                if last - time.time() < -loop_time:
                    func(self)

    def run(self) -> None:
        if self.RUNNING:
            raise RuntimeError("You can't run two instances at the same time.")
        i = 0
        self.RUNNING = True
        while self.RUNNING:
            try:
                self._step(i)
            except BaseException as e:
                print(e)
            i += 1

    def _run(self):
        if self.RUNNING:
            raise RuntimeError("You can't run two instances at the same time.")
        i = 0
        self.RUNNING = True
        while self.RUNNING:
            try:
                yield i, self._step(i)
            except BaseException as e:
                print(e)
                yield None
            i += 1

    def __iter__(self):
        for i, return_ in self._run():
            yield i, return_

    def _raw_request_post(
        self, path: str, /, annonymous: bool = False, **kwargs: Dict[str, str]
    ) -> requests.Response:
        print("request")
        url = self.server + path
        auth = {"Authorization": f"Bearer {self.token}"} if not annonymous else dict()
        response = requests.post(url, data=kwargs, headers=auth)

        if response.status_code == 429:
            self.stop()

        return response

    def post_status(self, text="Hello World from Mastodon API !") -> requests.Response:
        return self._raw_request_post("/api/v1/statuses", status=text)

    def looped_every(self, func: Callable, time: float = 60) -> Callable:
        if self.funcs.get(time) is None:
            self.funcs[time] = list()

        self.funcs[time].append((0, func))  # (last time executed, function)

        return func
