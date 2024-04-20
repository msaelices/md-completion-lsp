from pytest import raises
from simplelsp.jsonrpc import decode_msg, encode_msg, JsonRpcReader


def test_encode_msg():
    expected = 'Content-Length: 17\r\n\r\n{"testing": true}'
    assert expected == encode_msg({'testing': True})


def test_decode_msg():
    expected = {'testing': True}
    assert expected == decode_msg('Content-Length: 17\r\n\r\n{"testing": true}')
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
