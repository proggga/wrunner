'''Module with ProcessWorker'''
import subprocess
import time

from web.bufferreader import BufferReader
from web.eof_bufferreader import EofBufferReader


class ProcessWorker(object):
    '''Process worker: execute task'''

    def __init__(self):
        self._result_lines = None
        self._process = None
        self.split_char = '\n'

    def get_content(self):
        '''get content of last result lines'''
        return self._result_lines

    def execute(self, command):
        '''simple test with long command'''
        self._result_lines = ''
        self._process = subprocess.Popen(command, stdout=subprocess.PIPE,
                                         shell=True)
        buffer_reader = BufferReader(self._process, self.split_char)
        while self._process.poll() is None:
            for line in buffer_reader.read():
                yield self._store_and_return(line)
            time.sleep(0.1)
        buffer_reader = EofBufferReader(self._process,
                                        self.split_char,
                                        buffer_reader.get_buffer())
        for line in buffer_reader.read():
            yield self._store_and_return(line)

        self._clean()

    def _store_and_return(self, line):
        '''append line to array'''
        self._result_lines += line
        return line

    def _clean(self):
        del self._process
        self._process = None
