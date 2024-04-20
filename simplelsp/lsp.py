from io import TextIOBase
from pprint import pformat

from .jsonrpc import JsonRpcConsumer, Message, encode_msg


class LspConsumer(JsonRpcConsumer):
    def __init__(self, stream: TextIOBase, logger) -> None:
        self.logger = logger
        self.stream = stream

    def consume(self, msg: Message) -> None:
        self.logger.info(f'Consumed: {pformat(msg)}')
        response: Message | None = None
        match msg.method:
            case 'initialize':
                self.logger.info('Initializing')
                response = self.handle_initialize(msg)
            case 'shutdown':
                self.logger.info('Shutting down')
            case _:
                self.logger.info('Unknown method')

        if response:
            self.write_response(response)

    def write_response(self, response: Message) -> None:
        self.stream.write(encode_msg(response))

    def handle_initialize(self, msg: Message) -> Message:
        return Message({
            'method': 'initialize',
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
