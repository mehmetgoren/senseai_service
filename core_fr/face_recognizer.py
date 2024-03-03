import requests
from typing import List

from common.utilities import logger, config
from core_fr.models.face_recognition_response import FaceRecognitionResponse
from utils.json_serializer import deserialize_json
from utils.utilities import get_module_url


class DetectedFace:
    pred_cls_idx: int = 0
    pred_cls_name: str = ''
    pred_score: float = .0
    x1, y1, x2, y2 = 0, 0, 0, 0

    def format(self) -> str:
        return f'{self.pred_cls_idx}_{self.pred_cls_name}_{self.pred_score}'


class FaceRecognizer:
    def __init__(self):
        self.min_confidence = config.sense_ai.fr_threshold
        self.url = get_module_url('v1/vision/face/recognize')

    def predict(self, image_data: bytes) -> List[DetectedFace]:
        ret: List[DetectedFace] = []
        try:
            response_json = requests.post(self.url, files={'image': image_data}, data={'min_confidence': self.min_confidence}).text
            result = FaceRecognitionResponse()
            deserialize_json(response_json, result)
            for index, d in enumerate(result.predictions):
                df = DetectedFace()
                df.pred_score, df.pred_cls_idx, df.pred_cls_name = d.confidence, index, d.userid
                df.x1, df.y1, df.x2, df.y2 = d.x_min, d.y_min, d.x_max, d.y_max
                ret.append(df)
        except BaseException as ex:
            logger.error(f'an error occurred while face api call, ex: {ex}')

        return ret
