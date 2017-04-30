'''Module with ProcessWorker'''
import subprocess
import time


class ProcessWorker(object):
    '''Process worker: execute task'''

    def __init__(self):
        self._result_lines = None


    def get_content(self):
        '''get content of last result lines'''
        return self._result_lines


    def _store_line_and_return(self, line):
        '''append line to array'''
        self._result_lines += line
        return line


    def execute(self, command):
        '''simple test with long command'''
        self._result_lines = ''
        process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        buffer = ''
        while process.poll() is None:
            byte_data = process.stdout.read(8)
            buffer += byte_data.decode('utf-8')
            if '\n' in buffer:
                lines_array = buffer.split('\n')
                for line in lines_array[0:-1]:
                    yield self._store_line_and_return(line + '\n')
                buffer = lines_array[-1]
            time.sleep(0.1)
        end_of_line = process.stdout.read().decode('utf-8')
        if end_of_line:
            buffer += end_of_line
        lines_array = buffer.split('\n')
        for line in lines_array[0:-1]:
            yield self._store_line_and_return(line + '\n')
        if lines_array[-1]:
            yield self._store_line_and_return(lines_array[-1])
