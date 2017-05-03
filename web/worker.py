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

    def execute(self, command):
        '''simple test with long command'''
        self._result_lines = ''
        self._buffer = ''
        self._process = subprocess.Popen(command, stdout=subprocess.PIPE,
                                         shell=True)
        while self._process.poll() is None:
            for line in self._read_process_stdout():
                yield self._store_and_return(line)
            time.sleep(0.1)
        for line in self._read_process_stdout(read_to_end=True):
            yield self._store_and_return(line)

        del self._process
        del self._buffer
        self._buffer = None
        self._process = None

    def _read_process_stdout(self, read_to_end=False):
        eof = -1
        split_char = '\n'
        bytes_count = eof if read_to_end else 8
        self._read_buffer(bytes_count)
        if not self._buffer or (not read_to_end and
                                split_char not in self._buffer):
            return ()
        lines_array = list(self._buffer.split(split_char))
        self._buffer = lines_array.pop()
        result = [line + split_char for line in lines_array]
        if read_to_end and self._buffer:
            result.append(self._buffer)
        return result

    def _read_buffer(self, bytes_count):
        byte_data = self._process.stdout.read(bytes_count)
        self._buffer += byte_data.decode('utf-8')

    def _store_and_return(self, line):
        '''append line to array'''
        self._result_lines += line
        return line
