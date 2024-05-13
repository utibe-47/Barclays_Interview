import os
from gui.create_huey import create_huey_app
from gui.thermos import create_app
from gui.thermos.huey_config import config_huey


app = create_app(os.getenv('THERMOS_ENV') or 'prod')
huey = create_huey_app(config_huey)
