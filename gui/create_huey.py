from huey import RedisHuey


def create_huey_app(config):
    _storage_args = {
        'read_timeout': config.get('HUEY_STORAGE_READ_TIMEOUT', 1),
        'url': config.get('HUEY_STORAGE_URL', None),
        'blocking': config.get('HUEY_BLOCKING', None)
    }

    _huey = RedisHuey(
        name=config.get('HUEY_TASK_QUEUE_NAME', 'SINGULARITY'),
        results=config.get('HUEY_RESULTS', True),
        store_none=config.get('HUEY_STORE_NONE', False),
        immediate=config.get('HUEY_IMMEDIATE', False),
        **_storage_args
    )

    return _huey
