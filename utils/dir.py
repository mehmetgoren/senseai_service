import os
import sys

from common.utilities import logger
from common.config import Config


def create_dir_if_not_exists(directory: str):
    if not os.path.exists(directory):
        logger.warning(f'creating directory: {directory}')
        os.makedirs(directory)


def get_root_path_for_senseai(cnfg: Config) -> str:
    dir_paths = cnfg.general.dir_paths
    if len(dir_paths) == 0:
        logger.fatal('config.general.dir_paths is empty, the program will be terminated')
        sys.exit('config.general.dir_paths is empty')
    root_path = dir_paths[0]
    return root_path
