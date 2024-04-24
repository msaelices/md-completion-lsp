from __future__ import annotations

import json
from typing import Protocol

SEP = b'\r\n'
HEADER_SEP = b'\r\n\r\n'
CONTENT_LENGTH = b'Content-Length'


class Message(dict):
    """A JSON-RPC message."""

    @property
    def id(self) -> int:
        return self['id']

    @property
    def method(self) -> str | None:
        return self.get('method', None)

    @property
    def params(self) -> dict:
        return self['params']


class JsonRpcConsumer(Protocol):
    """A consumer of JSON-RPC messages."""

    def consume(self, msg: Message) -> None:
        ...


class JsonRpcReader:
    """Reads JSON-RPC messages from a stream and feeds them to a consumer."""

    def __init__(self, consumer: JsonRpcConsumer):
        self.buffer = b''
        self.consumer = consumer

    def feed(self, data: bytes) -> None:
        self.buffer += data
        if is_msg(self.buffer):
            msg = decode_msg(self.buffer)
            self.consumer.consume(msg)
            self.buffer = b''


class JsonRpcWriter:
    pass


def get_header_key(header: bytes, key: bytes) -> bytes:
    """Return the value of the key in the header."""
    try:
        return header.split(key + b':')[1].split(SEP)[0].strip()
    except IndexError:
        raise ValueError(f'Key {key} not found in header')


def is_msg(data: bytes) -> bool:
    """Return a boolean indicating if the message has been found."""
    try:
        header, content = data.split(HEADER_SEP, 1)
    except ValueError:
        return False
    if CONTENT_LENGTH not in header:
        return False
    content_length = int(get_header_key(header, CONTENT_LENGTH))
    return content_length == len(content)


def encode_msg(msg: Message) -> str:
    try:
        serialized = json.dumps(msg)
    except TypeError:
        raise ValueError('Message must be JSON serializable')
    return f'{CONTENT_LENGTH.decode()}: {len(serialized)}{HEADER_SEP.decode()}{serialized}'


def decode_msg(msg: bytes) -> Message:
    try:
        header, content = msg.split(HEADER_SEP, 1)
    except ValueError:
        raise ValueError('No header found in message')
    if CONTENT_LENGTH not in header:
        raise ValueError(f'Header must contain {CONTENT_LENGTH.decode()}')
    content_length = int(get_header_key(header, CONTENT_LENGTH))
    if content_length != len(content):
        raise ValueError(f'{CONTENT_LENGTH.decode()} does not match actual content length')

    return Message(**json.loads(content.decode()))
