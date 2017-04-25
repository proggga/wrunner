'''task for celery'''
from wrunner import celery_app
from web.worker import ProcessWorker


@celery_app.task(bind=True)
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
