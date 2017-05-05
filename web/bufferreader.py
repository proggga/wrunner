'''Module BufferReader'''


class BufferReader(object):
    '''Read from Popen process to buffer'''

    def __init__(self, process, split_char, buffer=''):
        self._process = process
        self._split_char = split_char
        self._buffer = buffer
        self.bytes_count = 8
        self.lines_array = []

    def read(self):
        '''read from buffer and return lines'''
        self._read_stdout()  # reading from buffer
        if self._need_skip_reading():
            return ()
        self.lines_array = self._split_buffer_to_lines()
        result = self._format_result()
        return result

    def _need_skip_reading(self):
        return bool(not self._buffer)

    def _split_buffer_to_lines(self):
        '''split buffer by separator and store last line as buffer'''
        lines = list(self._buffer.split(self._split_char))
        self._buffer = lines.pop()
        return lines

    def _format_result(self):
        '''format result from buffer'''
        return self.lines_array

    def get_buffer(self):
        '''return stored buffer'''
        return self._buffer

    def _read_stdout(self):
        byte_data = self._process.stdout.read(self.bytes_count)
        self._buffer += byte_data.decode('utf-8')
