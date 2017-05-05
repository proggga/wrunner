'''task for celery'''
from celery.task import task
from web.worker import ProcessWorker


@task(bind=True)
def execute_command_task(request, command):
    '''execute command in celery and update result by progress'''
    print("request, command:", request, command)
    pworker = ProcessWorker()
    result = 'started command: {}\n'\
             .format(command)
    execute_command_task.update_state(state='PROGRESS',
                                      meta={'stdout': result})
    for line in pworker.execute(command):
        result += line + '\n'
        execute_command_task.update_state(state='PROGRESS',
                                          meta={'stdout': result})
    return {'stdout': result}
