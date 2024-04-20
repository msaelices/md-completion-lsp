#!/usr/bin/env python3

import logging
import sys

from jsonrpc import JsonRpcReader, JsonRpcConsumer


logging.basicConfig(
    filename='output.log',
    level=logging.DEBUG,
)

logger = logging.getLogger(__name__)


class LSPConsumer(JsonRpcConsumer):

    def consume(self, msg: dict) -> None:
        logger.info(f'Consumed: {msg}')


def main():
    reader = JsonRpcReader(consumer=LSPConsumer())
    while True:
        data = sys.stdin.buffer.read(10).decode()
        reader.feed(data)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.error(f'Error in main: {e}')
