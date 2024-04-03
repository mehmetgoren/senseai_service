import os
from enum import Enum
from threading import Thread

from common.data.service_repository import ServiceRepository
from common.utilities import config, crate_redis_connection, RedisDb
from utils.dir import get_root_path_for_senseai


def register_senseai_service(service_name: str, instance_name: str, description: str):
    connection_main = crate_redis_connection(RedisDb.MAIN)
    service_repository = ServiceRepository(connection_main)
    service_repository.add(service_name, instance_name, description)
    return connection_main


class EventChannels(str, Enum):
    read_service = 'read_service'
    snapshot_in = 'snapshot_in'
    snapshot_out = 'snapshot_out'
    face_train_request = 'face_train_request'
    face_train_response = 'face_train_response'
    frtc = 'frtc'


def get_module_url(module_name: str) -> str:
    c = config.sense_ai
    return f'http://{c.host}:{c.port}/{module_name}'


def start_thread(fn, args):
    th = Thread(target=fn, args=args)
    th.daemon = True
    th.start()


def get_train_dir_path() -> str:
    x = get_root_path_for_senseai(config)
    y = os.path.join(x, 'ai', 'face', 'train')
    return y

