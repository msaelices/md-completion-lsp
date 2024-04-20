from jsonrpc import JsonRpcConsumer


class LspConsumer(JsonRpcConsumer):
    def __init__(self, logger) -> None:
        self.logger = logger

    def consume(self, msg: dict) -> None:
        self.logger.info(f'Consumed: {msg}')
        # TODO: Implement
