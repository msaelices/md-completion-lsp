from __future__ import annotations

from typing import Any


def encode_msg(msg: str) -> str:
    return f'Content-Length: {len(msg)}\r\n\r\n{msg}'

def decode_msg(msg: str) -> Any:
    return msg.split('\r\n\r\n', 1)[1]

