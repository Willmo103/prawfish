# Package: prawfish
import os
BASE_FILE_PATH = os.path.abspath(__file__).replace(os.path.basename(__file__), "")

from . import config

# Pacakge global variables
CONFIG = config.Config.try_build_config()
REDDIT = None
DATABASE_URL = None

# initialize the config and reddit instance
if CONFIG:
    DATABASE_URL = CONFIG.database_url()
    REDDIT = CONFIG.build_reddit_instance()

# determine if the package is running in a docker container
# if so, use the docker container's environment variables
# if not, use the local environment variables
# if "DOCKER" in os.environ:
