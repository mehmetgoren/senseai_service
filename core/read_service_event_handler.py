import base64
import json
from typing import List

from common.event_bus.event_bus import EventBus
from common.event_bus.event_handler import EventHandler
from common.utilities import logger
from core.detector import Detector
from utils.detection_result import DetectionResult
from utils.utilities import EventChannels, start_thread


class ReadServiceEventHandler(EventHandler):
    def __init__(self, detector: Detector):
        self.detector = detector
        self.encoding = 'utf-8'
        self.publisher = EventBus(EventChannels.snapshot_out)
        self.module = detector.module.name  # i.e. 'od', 'fr', 'alpr' etc.

    def handle(self, dic: dict):
        if dic is None or dic['type'] != 'message':
            return

        start_thread(self._handle, [dic])

    def _handle(self, dic: dict):
        try:
            data: bytes = dic['data']
            # todo: remove it if it is not necessary
            dic = json.loads(data.decode(self.encoding))
            name = dic['name']
            source_id = dic['source_id']
            base64_image = dic['base64_image']
            ai_clip_enabled = dic['ai_clip_enabled']

            base64_decoded: bytes = base64.b64decode(base64_image)

            results: List[DetectionResult] = self.detector.detect(base64_decoded, source_id)
            if len(results) > 0:
                detected_dic_list = []
                for r in results:
                    box = {'x1': r.x1, 'y1': r.y1, 'x2': r.x2, 'y2': r.y2}
                    dic_result = {'label': r.label, 'score': r.score, 'box': box}
                    detected_dic_list.append(dic_result)

                dic = {'module': self.module, 'name': name, 'source_id': source_id, 'base64_image': base64_image, 'ai_clip_enabled': ai_clip_enabled,
                       'detections': detected_dic_list}
                event = json.dumps(dic)
                self.publisher.publish(event)
            else:
                logger.info(f'(source {name}) detected nothing')
        except BaseException as ex:
            logger.error(f'an error occurred while handling an ai module request by SenseAI, err: {ex}')
