'''test task with exec'''
import unittest.mock as mock
import pytest
from django.test import override_settings
from web.tasks import execute_command_task


@mock.patch('web.tasks.execute_command_task.update_state')
@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
@pytest.mark.django_db
def test_create_task(update_state_method):
    '''test task created and return progress'''
    command = 'echo "This is first line"; sleep 0.1; '\
              'echo "but this is next line"; sleep 0.1; '\
              'echo "and the end of text"; sleep 0.1;'\
              'echo -n "done"'
    task = execute_command_task.delay(command)
    calls = []
    result = ''
    result += 'started command: {}'.format(command)
    calls.append(mock.call(state='PROGRESS', meta={'stdout': result}))
    result += 'This is first line\n'
    calls.append(mock.call(state='PROGRESS', meta={'stdout': result}))
    result += 'but this is next line\n'
    calls.append(mock.call(state='PROGRESS', meta={'stdout': result}))
    result += 'and the end of text\n'
    calls.append(mock.call(state='PROGRESS', meta={'stdout': result}))
    result += 'done'
    calls.append(mock.call(state='PROGRESS', meta={'stdout': result}))
    update_state_method.assert_has_calls(calls)
    assert task.status == 'SUCCESS'
