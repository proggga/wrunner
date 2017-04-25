'''test task with exec'''
import pytest
import time
import mock

@pytest.mark.django_db
def test_create_task(celery_worker):
    with mock.patch()
    taskk = execute_command_task('ps aux')
    print(taskk, taskk.status)
    execute_command_task.app.worker_main()
    assert False

# @pytest.mark.django_dbt
@pytest.mark.skip('shitless')
def test_view_genearate_random_task(celery_app, celery_worker):
    '''test main view response'''
    command = 'echo "This is first line"; sleep 0.1; '\
              'echo "but this is next line"; sleep 0.1; '\
              'echo "and the end of text"; sleep 0.1;'\
                'echo "done"'
    # help(celery_app)
    from web.tasks import execute_command_task

    @celery_app.task
    def execute_ct(requst, command):
        return command.replace('\n','QQQ')

    # task = execute_command_task.delay(command)
    T100 = execute_ct.delay('', command)
    # task.app = celery_app
    time.sleep(3)
    print(T100, T100.status, T100.result)
    # help(task)
    assert False
    # assert task.status == ''
    # assert 'stdout' in json.loads(AsyncResult(url_hash).result).keys()
