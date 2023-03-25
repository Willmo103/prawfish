from . import config

CONFIG = config.Config.try_build_config()
DATABASE_URL = None

if CONFIG:
    DATABASE_URL = CONFIG.database_url()
