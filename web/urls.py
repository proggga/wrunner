'''Url list'''
from django.conf.urls import url
import web.views as views

urlpatterns = [  # pylint: disable=invalid-name
    url(r'start$', views.start_view, name='task-create-startpage'),
    url(r'status/(?P<task_id>[a-zA-Z0-9\-]+)',
        views.get_data, name='task-status'),
]
