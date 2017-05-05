'''Test EofBufferReader'''
import mock
from web.eof_bufferreader import EofBufferReader


def test_read_simple_data():
    """test BR reads 'simple data' from stdout"""
    attrs = {'stdout.read.return_value': b'simple data\n'}
    process = mock.Mock(**attrs)
    eof_breader = EofBufferReader(process, '\n')
    lines = eof_breader.read()
    assert lines[0] == 'simple data'
    assert len(lines) == 1


def test_read_simple_to_eof():
    """test BR reads 'simple data and last data' from stdout"""
    attrs = {'stdout.read.return_value': b'simple data\nneed_read_too'}
    process = mock.Mock(**attrs)
    eof_breader = EofBufferReader(process, '\n')
    lines = eof_breader.read()
    assert lines[0] == 'simple data'
    assert lines[1] == 'need_read_too'
    assert len(lines) == 2
