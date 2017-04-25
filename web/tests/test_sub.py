'''test for subprocess'''
import os
from web.worker import ProcessWorker


# Create your tests here.
def test_execute_command():
    '''simple test with long command'''
    os.environ['DJANGO_SETTINGS_MODULE'] = 'web.settings'
    command = 'echo "This is first line"; sleep 1; '\
              'echo "but this is next line"; sleep 3; '\
              'echo "and the end of text"; sleep 3;'\
              'echo "done"'
    pworker = ProcessWorker()
    shouldbe_lines = 'This is first line\n'\
                     'but this is next line\n'\
                     'and the end of text\n'\
                     'done\n'
    shouldbe_lines_array = [line + '\n' for line in shouldbe_lines.split('\n')
                            if line]
    for line in pworker.execute(command):
        assert line == shouldbe_lines_array.pop(0)
    assert pworker.result_lines == shouldbe_lines
