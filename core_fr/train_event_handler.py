import json

from common.event_bus.event_bus import EventBus
from common.event_bus.event_handler import EventHandler
from common.utilities import logger
from core_fr.face_trainer import FaceTrainer
from utils.utilities import start_thread, EventChannels


class TrainEventHandler(EventHandler):

    def handle(self, dic: dict):
        if dic is None or dic['type'] != 'message':
            return

        start_thread(_train, args=[])


def _train():
    result = True
    try:
        trainer = FaceTrainer()
        trainer.fit()
    except BaseException as ex:
        logger.error(f'an error occurred during the face training, err: {ex}')
        result = False

    if result:
        internal_eb = EventBus(EventChannels.frtc)
        internal_eb.publish_async(json.dumps({'reloaded': result}))

    event_bus = EventBus(EventChannels.face_train_response)
    event = json.dumps({'result': result})
    event_bus.publish(event)
    logger.info('training complete and the event was published')
