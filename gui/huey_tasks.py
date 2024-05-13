import sys
from os.path import dirname, abspath
from huey import crontab
from datetime import datetime

sys.path.append(dirname(dirname(abspath(__file__))))

from gui.app import huey, app
from gui.thermos.models import TaskMessage
from gui.thermos import db


class HueyTasks:

    current_user = None

    def __init__(self, curr_user=None):
        HueyTasks.current_user = curr_user

    @staticmethod
    def populate_message_db(task, signal, message):

        with app.app_context():
            tm = TaskMessage(message=message, task_id=task.id, signal=signal, date=datetime.now())
            db.session.add(tm)
            db.session.commit()
