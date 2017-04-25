'''task for celery'''
from wrunner import CELERY_APP
from web.worker import ProcessWorker


@CELERY_APP.task(bind=True)
def execute_command_task(request, command):
    '''execute command in celery and update result by progress'''
    print(request)
    pworker = ProcessWorker()
    result = 'started command: {}'\
             .format(command)
    execute_command_task.update_state(state='PROGRESS',
                                      meta={'stdout': result})
    for line in pworker.execute(command):
        result += line
        execute_command_task.update_state(state='PROGRESS',
                                          meta={'stdout': result})
    return {'stdout': result}
