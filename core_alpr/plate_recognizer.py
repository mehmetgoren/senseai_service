from typing import List

import requests

from common.utilities import logger
from core_alpr.models.alpr_response import AlprResponse
from utils.detections import DetectionBox, DetectionResult
from utils.json_serializer import deserialize_json
from utils.utilities import get_module_url


class PlateRecognizer:
    def __init__(self, alpr_threshold: float):
        self.min_confidence = alpr_threshold
        self.url = get_module_url('v1/vision/alpr')

    # noinspection DuplicatedCode
    def recognize(self, image_data: bytes, detected_by: str) -> List[DetectionResult]:
        ret: List[DetectionResult] = []
        try:
            response_json = requests.post(self.url, files={'image': image_data}, data={'min_confidence': self.min_confidence}).text
            result = AlprResponse()
            deserialize_json(response_json, result)
            if not result.success or result.predictions is None:
                logger.error(f'an error occurred while alpr api call, source: {detected_by}, message: {result.message}')
                return ret
            predictions = result.predictions
            for p in predictions:
                cls_idx = 0
                box = DetectionBox()
                box.x1, box.y1, box.x2, box.y2 = p.x_min, p.y_min, p.x_max, p.y_max
                r = DetectionResult()
                r.box = box
                r.pred_cls_name, r.pred_cls_idx, r.pred_score = p.label, cls_idx, p.confidence
                ret.append(r)
        except BaseException as ex:
            logger.error(f'an error occurred while alpr api call, source: {detected_by}, ex: {ex}')
        return ret
