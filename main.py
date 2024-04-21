#!/usr/bin/env python3

from __future__ import annotations

import logging
import sys

from simplelsp.jsonrpc import JsonRpcReader
from simplelsp.lsp import LspConsumer


logging.basicConfig(
    filename='output.log',
    level=logging.DEBUG,
)

logger = logging.getLogger(__name__)


def main():
    consumer = LspConsumer(stream=sys.stdout, logger=logger)
    reader = JsonRpcReader(consumer=consumer)
    while True:
        data = sys.stdin.buffer.read(1).decode()
        reader.feed(data)


if __name__ == '__main__':
    main()
