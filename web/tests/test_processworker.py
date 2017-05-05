'''test system command executer'''
import os
from web.worker import ProcessWorker


def test_worker_return_stdout():
    '''simple test with execute long command'''
    os.environ['DJANGO_SETTINGS_MODULE'] = 'web.settings'
    bash_command = 'echo "start"; sleep 0.1; '\
                   'echo "message"; sleep 0.1; '\
                   'echo "fastmessage";'\
                   'echo "fastmessage";'\
                   'echo -n "end"'
    stdout_example = ['start',
                      'message',
                      'fastmessage',
                      'fastmessage',
                      'end']
    worker = ProcessWorker()
    result_array = []
    for current_line in worker.execute(bash_command):
        result_array.append(current_line)
    assert stdout_example == result_array
    assert worker.get_content() == ''.join(stdout_example)
