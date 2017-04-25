from django.conf.urls import url
import web.views as views

urlpatterns = [  # pylint: disable=invalid-name
    url(r'^$', views.index_view),
    url(r'status/(?P<task_id>[a-zA-Z0-9\-]+)', views.get_data, name='task-status'),
]
