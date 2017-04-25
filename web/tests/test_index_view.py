'''test main view'''
import re
from django.urls import reverse
from django.test import Client
from wrunner import celery_app
from celery.result import AsyncResult
import pytest


@pytest.mark.django_db()
def test_view_genearate_random_task():
    '''test main view response'''
    celery_app.conf.update(CELERY_ALWAYS_EAGER=True)
    url = reverse('task-create-indexpage')
    client = Client()
    response = client.get(path=url)
    match_res = re.match(r'<h1>Hello started task '
                         r'<a href=".*status/([a-zA-Z0-9\-]+)">'
                         r'([a-zA-Z0-9\-]+)</a></h1',
                         response.content.decode('utf-8'))
    assert match_res
    url_hash = match_res.group(1)
    text_hash = match_res.group(2)
    hash_lenght = len(url_hash)
    assert hash_lenght > 0
    assert re.match(r'^[a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}'
                    r'-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12}$',
                    url_hash)
    assert url_hash == text_hash
    assert AsyncResult(url_hash).result == ''
