from __future__ import annotations

import json
from typing import Any


def encode_msg(msg: Any) -> str:
    try:
        serialized = json.dumps(msg)
    except TypeError:
        raise ValueError('Message must be JSON serializable')
    return f'Content-Length: {len(serialized)}\r\n\r\n{serialized}'

def decode_msg(msg: str) -> Any:
    try:
        header, content = msg.split('\r\n\r\n', 1)
    except ValueError:
        raise ValueError('No header found in message')
    if 'Content-Length' not in header:
        raise ValueError('Header must contain Content-Length')
    content_length = int(header.split('Content-Length: ')[1].split('\r\n')[0])
    if content_length != len(content):
        raise ValueError('Content-Length does not match actual content length')
    return json.loads(content)

