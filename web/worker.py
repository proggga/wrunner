'''Module with ProcessWorker'''
import subprocess
import time


class ProcessWorker(object):
    '''Process worker: execute task'''

    def __init__(self):
        self.result_lines = None

    def append_line(self, line):
        '''append line to array'''
        self.result_lines += line
        return line

    def execute(self, command):
        '''simple test with long command'''
        self.result_lines = ''
        process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        buffer = ''
        while process.poll() is None:
            byte_data = process.stdout.read(8)
            buffer += byte_data.decode('utf-8')
            if '\n' in buffer:
                lines_array = buffer.split('\n')
                for line in lines_array[0:-1]:
                    yield self.append_line(line + '\n')
                buffer = lines_array[-1]
            time.sleep(0.1)
        end_of_line = process.stdout.read().decode('utf-8')
        if end_of_line:
            buffer += end_of_line
        lines_array = buffer.split('\n')
        for line in lines_array[0:-1]:
            yield self.append_line(line + '\n')
        if lines_array[-1]:
            yield self.append_line(lines_array[-1])
