from typing import Any

import re
import requests


TOKEN_FORMAT = re.compile(r"^[A-Za-z0-9\-_]{43}$")


class Client:
    def __init__(self, /, token: str) -> None:
        if not isinstance(token, str):
            raise TypeError(f"Token type `{type(token)}` not supported. Must be a str.")
        if len(token) != 43:
            raise ValueError(f"Token lenght must be 43 characters not {len(token)}.")
        if not TOKEN_FORMAT.match(token):
            raise ValueError(f"Token doesn't match the format.")
        self.token = token

        self.RUNNING = False


    def __repr__(self) -> str:
        return f"Client(token='{self.token[:7] + '*'*(20-7) + self.token[20:]}')"

    def stop(self) -> None:
        self.RUNNING = False

    def _step(self, i: int = None) -> Any:
        pass

    def run(self) -> None:
        if self.RUNNING:raise RuntimeError("You can't run two instances at the same time.")
        i = 0
        self.RUNNING = True
        while self.RUNNING:
            try:
                self._step(i)
            except BaseException as e:
                print(e)
            i += 1
    
    def _run(self):
        if self.RUNNING:raise RuntimeError("You can't run two instances at the same time.")
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
    
