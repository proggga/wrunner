'''Module with ProcessWorker

contributors:
* Mikhail Fesenko

Copyright [2017] [MKFESENKO]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
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
            buffer += process.stdout.read(8).decode('utf-8')
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
