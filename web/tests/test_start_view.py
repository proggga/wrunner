'''test main view'''
import re
from django.urls import reverse
from django.test import Client


def test_start_view_content():
    '''test /start return content with uuids'''
    url = reverse('task-create-startpage')
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
