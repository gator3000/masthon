from typing import Dict

import requests


class Client:
    def __init__(self, /, token: str) -> None:
        if not isinstance(token, str):
            raise TypeError(f"Token type `{type(token)}` not supported. Must be a str.")
        self.token = token

        self.infos = self._get_infos()
    
    def __repr__(self) -> str:
        return f"Client(token='{"*"*5 + self.token[5:]}')"
    
    def _get_infos(self) -> Dict[str, object]:
        _return = {}
        return _return
    
    def __getitem__(self, item: str) -> object:
        if not isinstance(item, str):
            raise TypeError(f"Infos name type `{type(item)}` not supported. Must be a str.")

        try:
            return self.infos[item]
        except KeyError:
            raise AttributeError(f"Info `{item}` not found.")
    
