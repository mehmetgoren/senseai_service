from typing import List

from redis.client import Redis

from common.data.ai_module_model import AiModuleModel
from common.data.base_repository import BaseRepository


class AiModuleRepository(BaseRepository):
    def __init__(self, connection: Redis):
        super().__init__(connection, 'ai_modules:')

    def _get_key(self, service_name: str) -> str:
        return f'{self.namespace}{service_name}'

    def add(self, name: str, description: str, enabled: bool, api_url: str, threshold: float, label_field: str,
            motion_detection_enabled: bool, persistence_enabled: bool, notification_enabled: bool):
        key = self._get_key(name)
        model = AiModuleModel()
        model.name = name
        model.description = description
        model.enabled = enabled
        model.api_url = api_url
        model.threshold = threshold
        model.label_field = label_field
        model.motion_detection_enabled = motion_detection_enabled
        model.persistence_enabled = persistence_enabled
        model.notification_enabled = notification_enabled
        dic = self.to_redis(model)
        self.connection.hset(key, mapping=dic)

    def check_sense_ai_default_modules(self) -> List[AiModuleModel]:
        all_modules = self.get_all()
        default_modules = [
            ('od', 'Object Detection', True, 'v1/vision/detection', 0.4, 'label', True, True, True),
            ('fd', 'Face Detection', False, 'v1/vision/face', 0.4, '', False, True, True),
            ('fr', 'Face Recognition', False, 'v1/vision/face/recognize', 0.4, 'userid', False, True, True),
            ('alpr', 'Automatic License Plate Recognition', False, 'v1/vision/alpr', 0.4, 'label', False, True, True),
            ('ocr', 'Optical Character Recognition', False, 'v1/vision/ocr', 0.4, 'label', False, True, True),
        ]
        for module in default_modules:
            if not any(x.name == module[0] for x in all_modules):
                self.add(module[0], module[1], module[2], module[3], module[4], module[5], module[6], module[7], module[8])
        return all_modules

    def get_all(self) -> List[AiModuleModel]:
        models: List[AiModuleModel] = []
        keys = self.connection.keys(self.namespace + '*')
        for key in keys:
            dic = self.connection.hgetall(key)
            model: AiModuleModel = self.from_redis(AiModuleModel(), dic)
            models.append(model)
        return models

    def get(self, name: str) -> AiModuleModel:
        key = self._get_key(name)
        dic = self.connection.hgetall(key)
        ret = self.from_redis(AiModuleModel(), dic)
        if ret is None:
            ret = AiModuleModel()
        return ret
