from __future__ import annotations

from typing import TYPE_CHECKING
from io import TextIOBase

from .jsonrpc import JsonRpcConsumer, Message, encode_msg

if TYPE_CHECKING:
    from logging import Logger


class LspConsumer(JsonRpcConsumer):
    def __init__(self, stream: TextIOBase, logger: Logger) -> None:
        self.logger = logger
        self.stream = stream

    def consume(self, msg: Message) -> None:
        self.logger.info(f'Consumed: {msg}')
        response_msg: Message | None = None
        match msg.method:
            case 'initialize':
                self.logger.info('Initializing')
                response_msg = self.handle_initialize(msg)
            case 'shutdown':
                self.logger.info('Shutting down')
            case _:
                self.logger.info(f'Not implemented method: {msg.method}')

        if response_msg:
            self.write_response(msg, response_msg)

    def write_response(self, req_msg: Message, response_msg: Message) -> None:
        final_msg = Message(id=req_msg.id, jsonrpc='2.0', result=response_msg)
        encoded = encode_msg(final_msg)
        self.stream.write(encoded)
        self.stream.flush()
        self.logger.info(f'Wrote: {encoded}')


    def handle_initialize(self, msg: Message) -> Message:
        return Message({
            'capabilities': self._get_capabilities(),
            'serverInfo': {
                'name': 'simplelsp',
            },
        })

    def _get_capabilities(self):
        return {
            'codeActionProvider': False, # Actions to a fragment of code to refactor, fix or beautify it
            'codeLensProvider': {
                'resolveProvider': False,  # Like show git blame line or similar 
            },
            'completionProvider': {
                'resolveProvider': False,
                'triggerCharacters': ['.'],
            },
            'documentFormattingProvider': False,
            'documentHighlightProvider': False,
            'documentRangeFormattingProvider': False,
            'documentSymbolProvider': False,
            'definitionProvider': False,
            'executeCommandProvider': {
                'commands': [],
            },
            'hoverProvider': False,
            'referencesProvider': False,
            'renameProvider': False,
            'foldingRangeProvider': False,
            'signatureHelpProvider': {'triggerCharacters': ['(', ',', '=']},
            'textDocumentSync': {  # Defines how text documents are synced
                'change': 2, # 2 -> Incremental
                'openClose': False,
            },
            'workspace': {
                'workspaceFolders': {'supported': False, 'changeNotifications': False}
            },
        }
