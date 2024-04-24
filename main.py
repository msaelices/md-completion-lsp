#!/usr/bin/env python3

from __future__ import annotations

import argparse
import logging
import sys

from mdcompletion.jsonrpc import JsonRpcReader
from mdcompletion.lsp import LspConsumer

logger = logging.getLogger(__name__)


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--log-file', help='Log file path', default='mdcompletion.log')
    arg_parser.add_argument('--log-level', help='Log level', default='DEBUG', choices=('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'))
    args = arg_parser.parse_args()
    
    logging.basicConfig(
        filename=args.log_file,
        level=getattr(logging, args.log_level, logging.INFO),
    )
    consumer = LspConsumer(stream=sys.stdout, logger=logger)
    reader = JsonRpcReader(consumer=consumer)
    while True:
        data = sys.stdin.buffer.read(1).decode()
        reader.feed(data)


if __name__ == '__main__':
    main()
