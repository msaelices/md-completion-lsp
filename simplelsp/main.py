#!/usr/bin/env python3

import logging
import sys

from jsonrpc import encode_msg, decode_msg, is_msg


logging.basicConfig(
    filename='output.log',
    level=logging.DEBUG,
)

logger = logging.getLogger(__name__)


def main():
    while True:
        msg, has_more = next_message()
        while has_more:
            msg, has_more = next_message(msg)
        handle_message(msg)


def next_message(prev_data: str = '') -> tuple[str, bool]:
    """Read the next message from stdin. Return a boolean indicating if has more text to come."""
    data = prev_data + sys.stdin.buffer.read(10).decode()
    logger.debug(f'Next message: {data}')

    has_more = not is_msg(data)

    return data, has_more


def handle_message(msg: str) -> None:
    logger.info(f'Received: {msg}')
    try:
        data = decode_msg(msg)
        logger.info(f'Decoded data: {data}')
    except Exception as e:
        logger.error(f'Error decoding message: {e}')



if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.error(f'Error in main: {e}')
