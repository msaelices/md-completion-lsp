from __future__ import annotations

import json
from typing import Any

SEP = '\r\n'
HEADER_SEP = f'{SEP}{SEP}'
CONTENT_LENGTH = 'Content-Length'


def get_header_key(header: str, key: str) -> str:
    """Return the value of the key in the header."""
    try:
        return header.split(f'{key}:')[1].split(SEP)[0].strip()
    except IndexError:
        raise ValueError(f'Key {key} not found in header')


def is_msg(data: str) -> bool:
    """Return a boolean indicating if the message has been found."""
    try:
        header, content = data.split(HEADER_SEP, 1)
    except ValueError:
        return False
    if CONTENT_LENGTH not in header:
        return False
    content_length = int(get_header_key(header, CONTENT_LENGTH))
    return content_length == len(content)


def encode_msg(msg: Any) -> str:
    try:
        serialized = json.dumps(msg)
    except TypeError:
        raise ValueError('Message must be JSON serializable')
    return f'{CONTENT_LENGTH}: {len(serialized)}\r\n\r\n{serialized}'


def decode_msg(msg: str) -> Any:
    try:
        header, content = msg.split(HEADER_SEP, 1)
    except ValueError:
        raise ValueError('No header found in message')
    if CONTENT_LENGTH not in header:
        raise ValueError(f'Header must contain {CONTENT_LENGTH}')
    content_length = int(get_header_key(header, CONTENT_LENGTH))
    if content_length != len(content):
        raise ValueError(f'{CONTENT_LENGTH} does not match actual content length')
    return json.loads(content)

