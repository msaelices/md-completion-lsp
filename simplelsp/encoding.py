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
    return json.loads(msg.split('\r\n\r\n', 1)[1])

