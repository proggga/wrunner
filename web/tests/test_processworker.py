'''test system command executer'''
import os
import re
from web.worker import ProcessWorker


def test_execute_command():
    '''simple test with long command'''
    os.environ['DJANGO_SETTINGS_MODULE'] = 'web.settings'
    long_bash_command = 'echo "start"; sleep 0.1; '\
                        'echo "message"; sleep 0.1; '\
                        'echo -n "end"'
    result_example = ['start\n',
                      'message\n',
                      'end']
    worker = ProcessWorker()
    line_num = 0
    max_count = len(result_example)
    for line in worker.execute(long_bash_command):
        assert line_num < max_count, 'Strange extra result: "{}"'.format(line)
        assert line == result_example[line_num]
        line_num = line_num + 1
    assert line_num == max_count, 'Not all result returned'
    assert worker.result_lines == ''.join(result_example)
