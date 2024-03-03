from __future__ import annotations

import argparse
import json
import os
from types import SimpleNamespace
from typing import List
from redis import Redis
from enum import IntEnum
import platform


# it is readonly, but it is shown on redis as information
class ConfigRedis:
    def __init__(self):
        self.host: str = '127.0.0.1'
        self.port: int = 6379
        self.__init_values()

    def __init_values(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--redis-host')
        parser.add_argument('--redis-port')
        args = parser.parse_args()

        self.host: str = ''
        self.port: int = 0

        eh = os.getenv('REDIS_HOST', '')
        if len(eh) > 0:
            self.host = eh
        elif args.redis_host is not None and len(args.redis_host) > 0:
            self.host = args.redis_host
        else:
            self.host = '127.0.0.1'
        print(f'Redis host: {self.host}')

        ep = os.getenv('REDIS_PORT', '')
        if len(ep) > 0:
            self.port = int(ep)
        elif args.redis_port is not None and len(args.redis_port) > 0:
            self.port = int(args.redis_port)
        else:
            self.port = 6379
        print(f'Redis port: {self.port}')


config_redis = ConfigRedis()


class DbType(IntEnum):
    SQLite = 0
    MongoDB = 1


class DeviceType(IntEnum):
    PC = 0
    IOT = 1


class DeepStackPerformanceMode(IntEnum):
    Low = 0
    Medium = 1
    High = 2


class DeepStackDockerType(IntEnum):
    CPU = 0
    GPU = 1
    NVIDIA_JETSON = 2
    ARM64 = 3
    ARM64_SERVER = 4


class SenseAIType(IntEnum):
    CPU = 0
    GPU_CUDA_11_7 = 1
    GPU_CUDA_12_2 = 2
    ARM64 = 3
    RPI64 = 4


class ArchiveActionType(IntEnum):
    Delete = 0
    MoveToNewLocation = 1


class DeviceConfig:
    def __init__(self):
        self.device_name = platform.node()
        _, _, _, _, machine, _ = platform.uname()
        self.device_type = DeviceType.PC if 'x86' in machine else DeviceType.IOT


class JetsonConfig:
    def __init__(self):
        self.model_name: str = 'ssd-mobilenet-v2'


class TorchConfig:
    def __init__(self):
        self.model_name = 'ultralytics/yolov5'
        self.model_name_specific = 'yolov5x6'


class TensorflowConfig:
    def __init__(self):
        self.model_name = 'efficientdet/lite4/detection'
        self.cache_folder: str = '/mnt/sdc1/test_projects/tf_cache'


class CoralTPUConfig:
    def __init__(self):
        self.model_path = './models/edgetpu_model.tflite'
        self.labels_path = './models/edgetpu_labels.txt'


class SourceReaderConfig:
    def __init__(self):
        self.resize_img: bool = False
        self.buffer_size: int = 2
        self.max_retry: int = 150
        self.max_retry_in: int = 6  # hours


class GeneralConfig:
    def __init__(self):
        self.dir_paths: List[str] = []
        self.heartbeat_interval: int = 30


class DbConfig:
    def __init__(self):
        self.type: DbType = DbType.MongoDB
        self.connection_string = 'mongodb://localhost:27017'


class FFmpegConfig:
    def __init__(self):
        self.use_double_quotes_for_path: bool = False
        self.max_operation_retry_count: int = 10000000
        self.ms_init_interval: float = 3.  # ms prefix is for media server.
        self.watch_dog_interval: int = 23
        self.watch_dog_failed_wait_interval: float = 3.
        self.start_task_wait_for_interval: float = 1.
        self.record_concat_limit: int = 1
        self.record_video_file_indexer_interval: int = 60
        # 1024 - 65535
        self.ms_port_start: int = 7000  # for more info: https://www.thegeekdiary.com/which-network-ports-are-reserved-by-the-linux-operating-system/
        self.ms_port_end: int = 8000  # should be greater than total camera count


class AiConfig:
    def __init__(self):
        self.video_clip_duration: int = 10
        self.face_recog_mtcnn_threshold: float = .86
        self.face_recog_prob_threshold: float = .98
        self.plate_recog_instance_count: int = 2


class UiConfig:
    def __init__(self):
        self.gs_width: int = 4
        self.gs_height: int = 2
        self.booster_interval: float = .3
        self.seek_to_live_edge_internal: int = 30


class JobsConfig:
    def __init__(self):
        self.mac_ip_matching_enabled: bool = False
        self.mac_ip_matching_interval: int = 120
        self.black_screen_monitor_enabled: bool = False
        self.black_screen_monitor_interval: int = 600


class DeepStackConfig:
    def __init__(self):
        self.server_url: str = 'http://127.0.0.1'
        self.server_port: int = 1009
        self.performance_mode: DeepStackPerformanceMode = DeepStackPerformanceMode.Medium
        self.api_key: str = ''
        self.od_enabled: bool = True
        self.od_threshold: float = .45
        self.fr_enabled: bool = True
        self.fr_threshold: float = .7
        self.docker_type: DeepStackDockerType = DeepStackDockerType.GPU


class SenseAIConfig:
    def __init__(self):
        self.type: SenseAIType = SenseAIType.GPU_CUDA_12_2

        self.host: str = '127.0.0.1'
        self.port: int = 32168

        self.od_enabled: bool = True
        self.od_threshold: float = .4  # range 0.0 to 1.0. Default 0.4.

        self.fr_enabled: bool = True
        self.fr_threshold: float = .3

        self.alpr_enabled: bool = True
        self.alpr_confidence: float = .95  # range 0.0 to 1.0. Default 0.4.


class ArchiveConfig:
    def __init__(self):
        self.limit_percent: int = 95
        self.action_type: ArchiveActionType = ArchiveActionType.Delete
        self.move_location: str = ''


class SnapshotConfig:
    def __init__(self):
        self.process_count: int = 1
        self.overlay: bool = True
        self.meta_color_enabled: bool = False
        self.meta_color_count: int = 5
        self.meta_color_quality: int = 1


class HubConfig:
    def __init__(self):
        self.enabled: bool = False
        self.address: str = 'http://localhost:5268'
        self.token: str = ''
        self.web_app_address: str = 'http://localhost:8080'
        self.max_retry: int = 100


class Config:
    def __init__(self):
        self.device: DeviceConfig = DeviceConfig()
        self.jetson: JetsonConfig = JetsonConfig()
        self.torch: TorchConfig = TorchConfig()
        self.tensorflow: TensorflowConfig = TensorflowConfig()
        self.coral: CoralTPUConfig = CoralTPUConfig()
        self.source_reader: SourceReaderConfig = SourceReaderConfig()
        self.general: GeneralConfig = GeneralConfig()
        self.db: DbConfig = DbConfig()
        self.ffmpeg: FFmpegConfig = FFmpegConfig()
        self.ai: AiConfig = AiConfig()
        self.ui: UiConfig = UiConfig()
        self.jobs: JobsConfig = JobsConfig()
        self.deep_stack: DeepStackConfig = DeepStackConfig()
        self.sense_ai: SenseAIConfig = SenseAIConfig()
        self.archive: ArchiveConfig = ArchiveConfig()
        self.snapshot: SnapshotConfig = SnapshotConfig()
        self.hub: HubConfig = HubConfig()
        self.__connection: Redis | None = None

    @staticmethod
    def __get_redis_key():
        return 'config'

    @staticmethod
    def create():
        obj = Config()
        config_json = obj.__get_connection().get(obj.__get_redis_key())
        if config_json is not None:
            # noinspection PyTypeChecker
            simple_namespace = json.loads(config_json, object_hook=lambda d: SimpleNamespace(**d))
            obj.__dict__.update(simple_namespace.__dict__)
        return obj

    def to_json(self):
        dic = {}
        dic.update(self.__dict__)
        del dic['_Config__connection']
        return json.dumps(dic, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def __get_connection(self) -> Redis:
        if self.__connection is None:
            self.__connection = Redis(host=config_redis.host, port=config_redis.port, charset='utf-8', db=0,
                                      decode_responses=True)
        return self.__connection

    def save(self):
        self.__get_connection().set(self.__get_redis_key(), self.to_json())
