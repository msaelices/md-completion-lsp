#!/usr/bin/env python3

import logging
import sys

from jsonrpc import JsonRpcReader
from lsp import LspConsumer


logging.basicConfig(
    filename='output.log',
    level=logging.DEBUG,
)

logger = logging.getLogger(__name__)


def main():
    consumer = LspConsumer(stream=sys.stdout, logger=logger)
    reader = JsonRpcReader(consumer=consumer)
    while True:
        data = sys.stdin.buffer.read(10).decode()
        reader.feed(data)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.error(f'Error in main: {e}')
