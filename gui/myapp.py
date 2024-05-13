from os.path import dirname, abspath
import sys

from gui.thermos.monkey_patch import apply_monkey_patch

# from flask_script import Manager
# from flask_migrate import Migrate

sys.path.append(dirname(dirname(abspath(__file__))))

# from gui.thermos.monkey_patch import apply_monkey_patch
from gui.thermos.models import TaskMessage, FileSelection, User
from gui.thermos import db
from gui.app import app
from gui.app import huey

import gui.huey_tasks
import gui.huey_signals

app = apply_monkey_patch(app)
# manager = Manager(app)
# migrate = Migrate(app, db)


if __name__ == '__main__':
    # app.run(threaded=True, host='0.0.0.0')
    app.run(debug=True)
