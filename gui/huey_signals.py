from huey.signals import (SIGNAL_SCHEDULED, SIGNAL_EXECUTING, SIGNAL_RETRYING, SIGNAL_ERROR, SIGNAL_REVOKED,
                          SIGNAL_LOCKED, SIGNAL_COMPLETE)

from gui.app import huey
from gui.huey_tasks import HueyTasks


@huey.signal(SIGNAL_SCHEDULED, SIGNAL_EXECUTING, SIGNAL_RETRYING)
def signal_implementation_handler(signal, task, exc=None):
    if hasattr(task.args, '__iter__'):
        try:
            iter(task.args[0])
        except TypeError:
            task_name = str(task.args[0])
        else:
            try:
                task_name = str(task.args[0][0])
                if len(task_name) == 1:
                    task_name = str(task.args[0])
            except IndexError:
                try:
                    task_name = str(task.args[0])
                except (IndexError, TypeError):
                    task_name = str(task.args)
    else:
        task_name = str(task.args)

    if signal == SIGNAL_SCHEDULED:
        message = 'Task {} has been scheduled for implementation \n'.format(task_name)
    elif signal == SIGNAL_EXECUTING:
        message = 'Task {} is being executed.......\n'.format(task_name)
    else:
        message = 'Initial implementation of task {} failed and reimplementation has begun \n'.format(task_name)

    HueyTasks.populate_message_db(task, signal, message)


@huey.signal(SIGNAL_ERROR, SIGNAL_REVOKED, SIGNAL_LOCKED)
def signal_stop_or_error_handler(signal, task, exc=None):
    if hasattr(task.args, '__iter__'):
        try:
            task_name = str(task.args[0])
        except IndexError:
            task_name = str(task.args)
    else:
        task_name = str(task.args)

    if signal == SIGNAL_ERROR:
        message = 'Running task {} generated an error due to an unhandled exception leading to it being terminated ' \
                  'with error message {}: {}'.format(task_name, SIGNAL_ERROR, str(exc))
    elif signal == SIGNAL_REVOKED:
        message = 'Task {} has been revoked and will not be executed.'.format(task_name)
    else:
        message = 'Failed to acquire lock while implementing task {} leading to it being aborted'.format(task_name)

    HueyTasks.populate_message_db(task, signal, message)


@huey.signal(SIGNAL_COMPLETE)
def task_success(signal, task, exc=None):
    try:
        task_name = str(task.args[0])
    except IndexError:
        try:
            task_name = str(task.args[0][0])
        except (IndexError, TypeError):
            task_name = str(task)
    message = 'Running {} has been completed with message {}'.format(task_name, signal)
    HueyTasks.populate_message_db(task, signal, message)
