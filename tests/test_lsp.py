import logging
from io import TextIOBase
from simplelsp.jsonrpc import Message, decode_msg
from simplelsp.lsp import LspConsumer


class FakeStream(TextIOBase):
    def __init__(self) -> None:
        self.messages = []

    def write(self, s: str) -> int:
        self.messages.append(decode_msg(s))
        return len(s)


def test_initialize():
    stream = FakeStream()
    logger = logging.getLogger('dummy')
    logger.addHandler(logging.NullHandler())
    msg = Message({
        'method': 'initialize',
        'params': {
            'rootPath': None,
            'clientInfo':{
                'name': 'Neovim',
                'version': '0.9.4',
            },
            'trace': 'off',
            'capabilities': {
            },
            'workspaceFolders': None,
            'processId': 1234,
            'rootUri': None,
        },
        'jsonrpc': '2.0',
        'id': 1,
    })
    consumer = LspConsumer(stream=stream, logger=logger)
    consumer.consume(msg)
    assert stream.messages == [
        Message({
            'capabilities': {
                'codeActionProvider': False,
                'codeLensProvider': {'resolveProvider': False},
                'completionProvider': {
                     'resolveProvider': False,
                     'triggerCharacters': ['.'],
                },
                'definitionProvider': False,
                'documentFormattingProvider': False,
                'documentHighlightProvider': False,
                'documentRangeFormattingProvider': False,
                'documentSymbolProvider': False,
                'executeCommandProvider': {'commands': []},
                'foldingRangeProvider': False,
                'hoverProvider': False,
                'referencesProvider': False,
                'renameProvider': False,
                'signatureHelpProvider': {'triggerCharacters': ['(', ',', '=']},
                'textDocumentSync': {'change': 2, 'openClose': False},
                'workspace': {'workspaceFolders': {'changeNotifications': False, 'supported': False}},
            },
            'method': 'initialize',
            'serverInfo': {'name': 'simplelsp'},
        })
    ]

