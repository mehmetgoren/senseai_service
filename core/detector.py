import json
from datetime import datetime
from typing import List

import requests

from common.data.ai_module_model import AiModuleModel
from common.utilities import logger
from utils.detection_result import DetectionResult
from utils.utilities import get_module_url


# todo: change smpc go project to work with new DetectionResult
class Detector:
    def __init__(self, module: AiModuleModel):
        self.min_confidence = module.threshold
        self.url = get_module_url(module.api_url)
        self.label_field = module.label_field
        self.module = module

    def detect(self, image_data: bytes, detected_by: str) -> List[DetectionResult]:
        ret: List[DetectionResult] = []
        try:
            result: dict = requests.post(self.url, files={'image': image_data}, data={'min_confidence': self.min_confidence}).json()
            if not result['success']:
                # if 'error' in result:
                #     msg = result['error']
                # elif 'message' in result:
                #     msg = result['message']
                # else:
                #     msg = json.dumps(result)
                # logger.error(f'an error occurred while detection api call, source: {detected_by}, message: {msg} at {datetime.now()}')
                return ret
            if result['predictions'] is None:
                return ret
            predictions = result['predictions']
            for p in predictions:
                r = DetectionResult()
                if self.label_field not in p:
                    r.label = self.module.name
                else:
                    r.label = p[self.label_field]
                r.score = p['confidence']
                r.x1, r.y1, r.x2, r.y2 = p['x_min'], p['y_min'], p['x_max'], p['y_max']
                ret.append(r)
        except BaseException as ex:
            logger.error(f'an error occurred while detection api call, source: {detected_by}, ex: {json.dumps(ex.__dict__)} at {datetime.now()}')
        return ret
