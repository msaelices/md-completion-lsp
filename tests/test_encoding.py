from simplelsp.encoding import decode_msg, encode_msg


def test_encode_msg():
    expected = 'Content-Length: 17\r\n\r\n{"testing": true}'
    assert expected == encode_msg({'testing': True})

def test_decode_msg():
    expected = {'testing': True}
    assert expected == decode_msg('Content-Length: 17\r\n\r\n{"testing": true}')
