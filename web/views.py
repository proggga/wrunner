'''simple view'''
from celery.result import AsyncResult
from django.http import HttpResponse
from django.urls import reverse

from web.tasks import execute_command_task


def start_view(request):   # pylint: disable=unused-argument
    '''index view, return hello'''
    command = 'echo "This is first line"; sleep 1; '\
              'echo "but this is next line"; sleep 1; '\
              'echo "and the end of text"; sleep 1;'\
              'echo "done"'
    task = execute_command_task.delay(command)
    url = reverse('task-status', args=(task.task_id,))
    return HttpResponse('<h1>Hello started task <a href="{}">{}</a></h1>'
                        .format(url, task.task_id))


def get_data(request, task_id):  # pylint: disable=unused-argument
    '''data status of async command'''
    task_result = AsyncResult(task_id)

    return HttpResponse('<h1>Result of task {}</h1><br>{}'
                        .format(task_id, task_result.result))
