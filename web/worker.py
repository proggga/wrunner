'''Module with ProcessWorker'''
import subprocess
import time


class ProcessWorker(object):
    '''Process worker: execute task'''

    def __init__(self):
        self._result_lines = None
        self._buffer = None
        self._process = None

    def get_content(self):
        '''get content of last result lines'''
        return self._result_lines

    def _read(self, read_to_end=False):
        self._read_buffer(-1 if read_to_end else 8)
        if not self._buffer or (not read_to_end and '\n' not in self._buffer):
            return
        lines_array = list(self._buffer.split('\n'))
        lines_count = len(lines_array)
        self._buffer = lines_array.pop()
        for line in lines_array:
            yield self._store_line_and_return(line + '\n')
        if read_to_end and self._buffer:
            yield self._store_line_and_return(self._buffer)

    def _read_buffer(self, bytes_count):
        byte_data = self._process.stdout.read(bytes_count)
        self._buffer += byte_data.decode('utf-8')

    def _store_line_and_return(self, line):
        '''append line to array'''
        self._result_lines += line
        return line

    def execute(self, command):
        '''simple test with long command'''
        self._result_lines = ''
        self._buffer = ''
        self._process = subprocess.Popen(command, stdout=subprocess.PIPE,
                                         shell=True)
        while self._process.poll() is None:
            for line in self._read():
                yield line
            time.sleep(0.1)
        for line in self._read(read_to_end=True):
            yield line
        del self._process
        del self._buffer
        self._buffer = None
        self._process = None
