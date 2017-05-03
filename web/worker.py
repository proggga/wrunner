'''Module with ProcessWorker'''
import subprocess
import time


class ProcessWorker(object):
    '''Process worker: execute task'''

    def __init__(self):
        self._result_lines = None
        self._buffer = None
        self._process = None
        self.split_char = '\n'

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

        self._clean()

    def _read_process_stdout(self, read_to_end=False):
        self._read_buffer(read_to_end)  # reading from buffer
        if self._need_skip_reading(read_to_end):
            return ()
        lines_array = self._split_buffer_to_lines()
        result = self._format_result(lines_array, read_to_end)
        return result

    def _need_skip_reading(self, read_to_end):
        '''check if need skip read of stdout'''
        return (not self._buffer or
                (not read_to_end and self.split_char not in self._buffer))

    def _split_buffer_to_lines(self):
        '''split buffer by separator and store last line as buffer'''
        lines = list(self._buffer.split(self.split_char))
        self._buffer = lines.pop()
        return lines

    def _format_result(self, lines_array, read_to_end):
        '''format result from buffer'''
        lines = [line + self.split_char for line in lines_array]
        if read_to_end and self._buffer:
            lines.append(self._buffer)
        return lines

    def _read_buffer(self, read_to_end=False):
        eof = -1
        bytes_count = eof if read_to_end else 8
        byte_data = self._process.stdout.read(bytes_count)
        self._buffer += byte_data.decode('utf-8')

    def _store_and_return(self, line):
        '''append line to array'''
        self._result_lines += line
        return line

    def _clean(self):
        del self._process
        del self._buffer
        self._buffer = None
        self._process = None
