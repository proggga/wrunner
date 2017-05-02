'''test main view'''
import re
from django.urls import reverse
from django.test import Client
import pytest
from django.test import override_settings

@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
def test_start_view_content():
    '''test /start return content with uuids'''
    url = reverse('task-create-startpage')
    client = Client()
    response = client.get(path=url)
    match_res = re.match(r'<h1>Hello started task '
                         r'<a href=".*status/([a-zA-Z0-9\-]+)">'
                         r'([a-zA-Z0-9\-]+)</a></h1',
                         response.content.decode('utf-8'))
    assert match_res, 'Create task response not found by regexp'
    url_hash = match_res.group(1)
    text_hash = match_res.group(2)
    assert re.match(r'^[a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}'
                    r'-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12}$',
                    url_hash), 'UUID not valid uuid'
    assert url_hash == text_hash, 'Task uuid and uuid in link doesn\' equals'
