import base64
import json
from typing import List

from common.event_bus.event_bus import EventBus
from common.event_bus.event_handler import EventHandler
from common.utilities import logger
from core_alpr.plate_recognizer import PlateRecognizer
from utils.detections import DetectionResult
from utils.utilities import EventChannels, start_thread


class AlprReadServiceEventHandler(EventHandler):
    def __init__(self, recognizer: PlateRecognizer):
        self.recognizer = recognizer
        self.encoding = 'utf-8'
        self.publisher = EventBus(EventChannels.snapshot_out)

    def handle(self, dic: dict):
        if dic is None or dic['type'] != 'message':
            return

        start_thread(self._handle, [dic])

    # noinspection DuplicatedCode
    def _handle(self, dic: dict):
        try:
            data: bytes = dic['data']
            dic = json.loads(data.decode(self.encoding))
            name = dic['name']
            ai_clip_enabled = dic['ai_clip_enabled']

            # open it when you want to use snapshot_out
            # source_id = dic['source_id']
            # base64_image = dic['base64_image']
            source_id = dic['source']
            base64_image = dic['img']

            base64_decoded = base64.b64decode(base64_image)

            results: List[DetectionResult] = self.recognizer.recognize(base64_decoded, source_id)
            if len(results) > 0:
                detected_dic_list = []
                for r in results:
                    dic_box = {'x1': r.box.x1, 'y1': r.box.y1, 'x2': r.box.x2, 'y2': r.box.y2}
                    dic_result = {'pred_cls_name': r.pred_cls_name, 'pred_cls_idx': r.pred_cls_idx, 'pred_score': r.pred_score, 'box': dic_box}
                    detected_dic_list.append(dic_result)

                dic = {'name': name, 'source': source_id, 'img': base64_image, 'ai_clip_enabled': ai_clip_enabled, 'detections': detected_dic_list,
                       'channel': 'od_service', 'list_name': 'detected_objects'}
                event = json.dumps(dic)
                self.publisher.publish(event)
            else:
                logger.info(f'(camera {name}) recognized nothing')
        except BaseException as ex:
            logger.error(f'an error occurred while handling an ALPR request by SenseAI, err: {ex}')
