'''test for subprocess'''
import os
import re
from web.worker import ProcessWorker


def test_execute_command():
    '''simple test with long command'''
    os.environ['DJANGO_SETTINGS_MODULE'] = 'web.settings'
    command = 'echo "This is first line"; sleep 0.1; '\
              'echo "but this is next line"; sleep 0.1; '\
              'echo "and the end of text"; sleep 0.1;'\
              'echo -n "done\nhello"'
    pworker = ProcessWorker()
    should_lines = 'This is first line\n'\
                   'but this is next line\n'\
                   'and the end of text\n'\
                   'done\n'\
                   'hello'
    should_lines_array = [re.sub(r'\|$', '\n', line) for line in should_lines
                          .replace('\n', '|Q|').split('Q|') if line]
    for line in pworker.execute(command):
        assert line == should_lines_array.pop(0)
    assert pworker.result_lines == should_lines
