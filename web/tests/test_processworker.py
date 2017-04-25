'''test for subprocess'''
import os
import re
import pytest
from web.worker import ProcessWorker


# Create your tests here.
@pytest.mark.skip(reason="too long, check only before commit")
def test_execute_command():
    '''simple test with long command'''
    os.environ['DJANGO_SETTINGS_MODULE'] = 'web.settings'
    command = 'echo "This is first line"; sleep 1; '\
              'echo "but this is next line"; sleep 3; '\
              'echo "and the end of text"; sleep 3;'\
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
