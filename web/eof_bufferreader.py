'''Module EofBufferReader'''
from web.bufferreader import BufferReader


class EofBufferReader(BufferReader):
    '''Read from buffer to END (EOF)'''

    def __init__(self, *args, **kwargs):
        super(EofBufferReader, self).__init__(*args, **kwargs)
        read_to_eof = -1
        self.bytes_count = read_to_eof

    def _format_result(self):
        '''format result from buffer'''
        result = list(self.lines_array)
        if self._buffer:
            result.append(self._buffer)
            self._buffer = ''
        return result
