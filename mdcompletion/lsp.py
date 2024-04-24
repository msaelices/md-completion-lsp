from __future__ import annotations

from typing import TYPE_CHECKING
from io import TextIOBase

from .doc import Document
from .jsonrpc import JsonRpcConsumer, Message, encode_msg

if TYPE_CHECKING:
    from logging import Logger


class LspConsumer(JsonRpcConsumer):
    def __init__(self, stream: TextIOBase, logger: Logger, github_url: str = '') -> None:
        self.logger = logger
        self.stream = stream
        self.github_url = github_url
        self.documents: dict[str, Document] = {}

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
            case 'textDocument/didChange':
                self.logger.info('Document changed')
                response_msg = self.handle_did_change(msg)
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

    def handle_did_change(self, msg: Message) -> Message:
        doc_data = msg.params['textDocument']
        content_changes = msg.params['contentChanges']
        self.documents[doc_data['uri']].text = content_changes[0]['text']

    def handle_completion(self, msg: Message) -> Message:
        doc_data = msg.params['textDocument']
        position = msg.params['position']
        end_col = position['character']
        doc_line = self._get_doc_text_at(doc_data['uri'], position['line'], 0, end_col)
        start_col = max(0, doc_line.rfind('['))

        self.logger.debug(f'Line to complete: {doc_line}. Start col: {start_col}, end col: {end_col}')
        link_title = doc_line[start_col + 1:end_col - 1]
        prefix = link_title[:2].upper()

        match prefix:
            case 'PR':
                pr_number = link_title[2:]
                label = f'PR #{pr_number} link'
                text_to_insert = f'({self.github_url}/pull/{pr_number})'
            case _:
                label = ''
                text_to_insert = ''

        if not text_to_insert:
            return Message(isIncomplete=False, items=[])

        return Message(
            isIncomplete=False,
            items=[
                {
                    'label': label,
                    'kind': 18,
                    'insertText': text_to_insert,
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
                'change': 1, # 1 -> Full, 2 -> Incremental
                'openClose': True,
            },
            'workspace': {
                'workspaceFolders': {'supported': False, 'changeNotifications': False}
            },
        }

    def _get_doc_text_at(self, uri: str, line: int, start_col: int, end_col: int) -> str:
        doc = self.documents[uri]
        return doc.text_at(line, start_col, end_col)
