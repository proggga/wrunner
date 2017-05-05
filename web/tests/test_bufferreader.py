'''Test BufferReader'''
import mock
from web.bufferreader import BufferReader


def test_reads_one_line():
    """test reads 'simple data' from stdout"""
    attrs = {'stdout.read.return_value': b'simple data\n'}
    process = mock.Mock(**attrs)
    buf_reader = BufferReader(process, '\n')
    lines = buf_reader.read()
    assert lines[0] == 'simple data'


def test_reads_two_lines():
    """test reads two lines from stdout"""
    attrs = {'stdout.read.return_value': b'first line\nsecond line\n'}
    process = mock.Mock(**attrs)
    buf_reader = BufferReader(process, '\n')
    lines = buf_reader.read()
    assert lines[0] == 'first line'
    assert lines[1] == 'second line'


def test_reads_empty_buffer():
    """test reads empty data from stdout"""
    attrs = {'stdout.read.return_value': b''}
    process = mock.Mock(**attrs)
    buf_reader = BufferReader(process, '\n')
    lines = buf_reader.read()
    assert lines == ()


def test_reads_store_buffer():
    """test BR reads empty data from stdout"""
    attrs = {'stdout.read.return_value': b'line\nstored line'}
    process = mock.Mock(**attrs)
    buf_reader = BufferReader(process, '\n')
    lines = buf_reader.read()
    assert lines[0] == 'line'
    assert len(lines) == 1


def test_reads_with_some_buffer():
    """test BR reads empty data from stdout"""
    attrs = {'stdout.read.return_value': b'line\nbuff'}
    process = mock.Mock(**attrs)
    old_buffer = 'simple '
    buf_reader = BufferReader(process, '\n', buffer=old_buffer)
    lines = buf_reader.read()
    assert lines[0] == 'simple line'
    assert len(lines) == 1
