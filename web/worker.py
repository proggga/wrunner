'''Module with ProcessWorker'''
import subprocess
import time


class ProcessWorker(object):
    '''Process worker: execute task'''

    def __init__(self):
        self._result_lines = None
        self.buffer = None
        self.process = None

    def get_content(self):
        '''get content of last result lines'''
        return self._result_lines


    def _store_line_and_return(self, line):
        '''append line to array'''
        self._result_lines += line
        return line

    def read_lines_from_process_stdout(self, flush_buffer=False):
        bytes_count = 16 if flush_buffer else -1  # 16 bytes
        byte_data = self.process.stdout.read(bytes_count)
        self.buffer += byte_data.decode('utf-8')
        if '\n' in self.buffer or flush_buffer:
            lines_array = self.buffer.split('\n')
            if lines_array[-1] == '':
                del lines_array[-1]
                lines_array[-1] += '\n'
            lines_count = len(lines_array)
            if not flush_buffer:
                self.buffer = lines_array[-1]
                lines_count -= 1
            for i in range(lines_count):
                line = lines_array[i]
                if flush_buffer and i + 1 == lines_count and line != '':
                    line_return = ''
                else:
                    line_return = '\n'
                yield self._store_line_and_return(line + line_return)

    def execute(self, command):
        '''simple test with long command'''
        self._result_lines = ''
        self.buffer = ''
        self.process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        while self.process.poll() is None:
            for line in self.read_lines_from_process_stdout():
                yield line
            time.sleep(0.1)
        for line in self.read_lines_from_process_stdout(flush_buffer=True):
            yield line
        del self.process
        del self.buffer
        self.buffer = None
        self.process = None
