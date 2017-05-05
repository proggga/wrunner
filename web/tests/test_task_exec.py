'''test task with exec'''
from django.test import override_settings
import mock as mock
import pytest

from web.tasks import execute_command_task


@mock.patch('web.tasks.execute_command_task.update_state')
@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
@pytest.mark.django_db
def test_create_task(update_state_method):
    '''test task created and return progress'''
    command = 'echo "start"; sleep 0.1; '\
              'echo "message"; sleep 0.1; '\
              'echo -n "end"'
    task = execute_command_task.delay(command)
    calls = []
    result = ''
    result += 'started command: {}\n'.format(command)
    calls.append(mock.call(state='PROGRESS', meta={'stdout': result}))
    result += 'start\n'
    calls.append(mock.call(state='PROGRESS', meta={'stdout': result}))
    result += 'message\n'
    calls.append(mock.call(state='PROGRESS', meta={'stdout': result}))
    result += 'end\n'
    calls.append(mock.call(state='PROGRESS', meta={'stdout': result}))
    update_state_method.assert_has_calls(calls)
    assert task.status == 'SUCCESS'
