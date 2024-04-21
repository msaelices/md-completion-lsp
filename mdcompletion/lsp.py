from __future__ import annotations

from typing import TYPE_CHECKING
from io import TextIOBase

from .doc import Document
from .jsonrpc import JsonRpcConsumer, Message, encode_msg

if TYPE_CHECKING:
    from logging import Logger


class LspConsumer(JsonRpcConsumer):
    def __init__(self, stream: TextIOBase, logger: Logger) -> None:
        self.logger = logger
        self.stream = stream
        self.documents = {}

    def consume(self, msg: Message) -> None:
        self.logger.info(f'Consumed: {msg}')
        response_msg: Message | None = None
        match msg.method:
            case 'initialize':
                self.logger.info('Initializing')
                response_msg = self.handle_initialize(msg)
            case 'initialized':
                self.logger.info('Initialized')
            case 'textDocument/didOpen':
                self.logger.info('Document opened')
                response_msg = self.handle_did_open(msg)
            case 'textDocument/completion':
                self.logger.info('Completion')
                response_msg = self.handle_completion(msg)
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
                'name': 'mdcompletion',
            },
        })

    def handle_did_open(self, msg: Message) -> Message:
        doc_data = msg.params['textDocument']
        self.documents[doc_data['uri']] = Document(
            uri=doc_data['uri'],
            text=doc_data['text'],
        )

    def handle_completion(self, msg: Message) -> Message:
        # TODO: Implement completion logic
        return Message(
            isIncomplete=False,
            items=[
                {
                    'label': 'PR #1 link',
                    'kind': 18,
                    'insertText': '(http://github.com/msaelices/md-complation-lsp/pull/1)',
                },
            ],
        )

    def _get_capabilities(self):
        return {
            'codeActionProvider': False, # Actions to a fragment of code to refactor, fix or beautify it
            'codeLensProvider': {
                'resolveProvider': False,  # Like show git blame line or similar 
            },
            'completionProvider': {
                'resolveProvider': True,
                'triggerCharacters': [']'],
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
                'change': 2, # 1 -> Full, 2 -> Incremental
                'openClose': True,
            },
            'workspace': {
                'workspaceFolders': {'supported': False, 'changeNotifications': False}
            },
        }
