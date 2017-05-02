'''test status view'''
import re
import unittest.mock as mock
import pytest
from web.tasks import execute_command_task

from django.urls import reverse
from django.test import Client
from django.test import override_settings


@pytest.mark.django_db
def test_status_view_none_return():
    '''test status return content with uuids and status'''
    url = reverse('task-status', args=('12345678-1234-1234-1234-123456781234',))
    client = Client()
    response = client.get(path=url)
    match_res = re.match(r'<h1>Result of task 12345678-1234-1234-'
                         r'1234-123456781234</h1><br>(.*)',
                         response.content.decode('utf-8'))
    assert match_res
    assert match_res.group(1) == 'None'


@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
@pytest.mark.django_db
def test_result_status_of_completed_task():
    '''test task created and return progress'''
    task_id = '12345678-1234-1234-1234-123456781234'
    command = 'echo "Simple result of task";'
    eager_result = execute_command_task.apply_async(args=(command,),
                                                    task_id=task_id)
    url = reverse('task-status', args=(task_id,))
    client = Client()
    with mock.patch('web.views.AsyncResult') as asyncresult_class:
        asyncresult_class.return_value = eager_result
        response = client.get(path=url)
    match_res = re.match(r'<h1>Result of task 12345678-1234-1234-'
                         r'1234-123456781234</h1><br>(.*)',
                         response.content.decode('utf-8'))
    assert match_res
    message = {'stdout': 'started command: echo "Simple result of task";\n'
                         'Simple result of task\n'}
    assert match_res.group(1) == str(message)
