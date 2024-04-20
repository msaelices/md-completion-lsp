from pytest import raises
from simplelsp.jsonrpc import decode_msg, encode_msg, JsonRpcReader


def test_encode_msg():
    expected = 'Content-Length: 24\r\n\r\n{"method": "initialize"}'
    assert expected == encode_msg({'method': 'initialize'})


def test_decode_msg():
    expected = {'method': 'initialize'}
    decoded = decode_msg('Content-Length: 24\r\n\r\n{"method": "initialize"}')
    assert expected == decoded
    assert decoded.method == 'initialize'
    with raises(
        ValueError, match='No header found in message',
    ):
        decode_msg('{"testing": true}')
    with raises(
        ValueError, match='Header must contain Content-Length',
    ):
        decode_msg('Content-Type: json-rpc\r\n\r\n{"testing": true}')
    with raises(
        ValueError, match='Content-Length does not match actual content length'
    ):
        decode_msg('Content-Length: 17\r\n\r\n{"testing": false}')


def test_jsonrpc_reader():
    messages = []
    class Consumer:
        def consume(self, msg):
            messages.append(msg)
    reader = JsonRpcReader(consumer=Consumer())
    reader.feed('Content-Length: 17\r\n\r\n{"testing": true}')
    assert messages == [{'testing': True}]
