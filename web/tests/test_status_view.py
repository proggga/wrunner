'''test status view'''
import re
from django.urls import reverse
from django.test import Client
import pytest


@pytest.mark.django_db
def test_status_view_content():
    '''test status return content with uuids and status'''
    url = reverse('task-status', args=('12345678-1234-1234-1234-123456781234',))
    client = Client()
    response = client.get(path=url)
    match_res = re.match(r'<h1>Result of task 12345678-1234-1234-'
                         r'1234-123456781234</h1><br>(.*)',
                         response.content.decode('utf-8'))
    assert match_res
    assert match_res.group(1) == 'None'
