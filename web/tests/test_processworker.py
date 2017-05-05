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
    line_number = 0
    lines_count = len(stdout_example)
    for current_line in worker.execute(bash_command):
        assert line_number < lines_count, 'Strange extra result: "{}"'\
            .format(current_line)
        assert stdout_example[line_number] == current_line, \
            'Not equal example line and yield response'
        line_number = line_number + 1
    assert line_number == lines_count, 'Not all result returned'
    assert worker.get_content() == ''.join(stdout_example)
