'''test task with exec'''
from django.test import override_settings
from mock import patch
from mock import call

from web.tasks import execute_command_task


@patch('web.tasks.execute_command_task.update_state')
@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
def test_create_task(update_state_method):
    '''test task created and return progress'''
    command = 'example command'
    with patch('web.tasks.ProcessWorker.execute') as execute_method:
        execute_method.return_value = ['line1', 'line2']
        task = execute_command_task.delay(command)
    calls = []
    result = 'started command: {}\n'.format(command)
    calls.append(call(state='PROGRESS', meta={'stdout': result}))
    result = 'started command: {}\nline1\n'.format(command)
    calls.append(call(state='PROGRESS', meta={'stdout': result}))
    result = 'started command: {}\nline1\nline2\n'.format(command)
    calls.append(call(state='PROGRESS', meta={'stdout': result}))
    update_state_method.assert_has_calls(calls)
    assert task.status == 'SUCCESS'
