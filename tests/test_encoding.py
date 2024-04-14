from simplelsp.encoding import decode_msg, encode_msg


def test_encode_msg():
    expected = 'Content-Length: 17\r\n\r\n{"testing": true}'
    assert expected == encode_msg('{"testing": true}')

def test_decode_msg():
    expected = '{"testing": true}'
    assert expected == decode_msg('Content-Length: 17\r\n\r\n{"testing": true}')
