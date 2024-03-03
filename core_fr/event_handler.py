import base64
import json

from common.event_bus.event_bus import EventBus
from common.event_bus.event_handler import EventHandler
from common.utilities import logger, config
from core_fr.face_recognizer import FaceRecognizer

from utils.utilities import EventChannels, start_thread


class FrReadServiceEventHandler(EventHandler):
    def __init__(self):
        self.prob_threshold: float = config.deep_stack.fr_threshold
        self.encoding = 'utf-8'
        self.fr = FaceRecognizer()
        self.publisher = EventBus(EventChannels.snapshot_out)

    def handle(self, dic: dict):
        if dic is None or dic['type'] != 'message':
            return

        start_thread(self.__handle, [dic])

    # noinspection DuplicatedCode
    def __handle(self, dic: dict):
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
            results = self.fr.predict(base64_decoded)
            if len(results) == 0:
                logger.info(f'image contains no face for camera: {name}')
                return

            detected_faces = []
            face_logs = []
            for face in results:
                prob = face.pred_score
                if prob < self.prob_threshold:
                    logger.info(f'prob ({prob}) is lower than threshold: {self.prob_threshold} for {face.pred_cls_name}')
                    continue
                dic_box = {'x1': face.x1, 'y1': face.y1, 'x2': face.x2, 'y2': face.y2}
                detected_faces.append({'pred_score': prob, 'pred_cls_idx': face.pred_cls_idx, 'pred_cls_name': face.pred_cls_name, 'box': dic_box})
                face_logs.append({'pred_cls_name': face.pred_cls_name, 'pred_score': face.pred_score}),
            if len(detected_faces) == 0:
                logger.info('no detected face prob score is higher than threshold, this event will not be published')
                return

            dic = {'name': name, 'source': source_id, 'img': base64_image, 'ai_clip_enabled': ai_clip_enabled, 'detections': detected_faces,
                   'channel': 'fr_service', 'list_name': 'detected_faces'}
            event = json.dumps(dic)
            self.publisher.publish(event)
            logger.info(f'face: detected {json.dumps(face_logs)}')
        except BaseException as ex:
            logger.error(f'an error occurred while handling an facial-recognition request by SenseAI, err: {ex}')
