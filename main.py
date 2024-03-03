import sys
import time
from multiprocessing import Process

from core_alpr.event_handler import AlprReadServiceEventHandler
from core_alpr.plate_recognizer import PlateRecognizer
from docker_manager import DockerManager

from common.event_bus.event_bus import EventBus
from common.utilities import config, logger
from core_fr.event_handler import FrReadServiceEventHandler
from core_fr.train_event_handler import TrainEventHandler
from core_od.event_handler import OdReadServiceEventHandler
from core_od.object_detector import ObjectDetector
from utils.utilities import EventChannels, register_senseai_service, start_thread


def setup_alpr():
    logger.info('SenseAI ALPR service will start soon')
    alpr_recognizer = PlateRecognizer()
    event_bus = EventBus(EventChannels.read_service)  # No Motion Detection
    handler = AlprReadServiceEventHandler(alpr_recognizer)
    logger.info('SenseAI ALPR service will start soon')
    event_bus.subscribe_async(handler)
    sys.exit()


def setup_fr():
    def train_event_handler():
        logger.info('SenseAI face training event handler will start soon')
        eb = EventBus(EventChannels.fr_train_request)
        th = TrainEventHandler()
        eb.subscribe_async(th)

    start_thread(fn=train_event_handler, args=[])

    handler = FrReadServiceEventHandler()

    logger.info('SenseAI face recognition service will start soon')
    event_bus = EventBus(EventChannels.read_service)  # No Motion Detection
    event_bus.subscribe_async(handler)
    sys.exit()


def setup_od():
    detector = ObjectDetector()
    event_bus = EventBus(EventChannels.snapshot_in)
    handler = OdReadServiceEventHandler(detector)
    logger.info('SenseAI service will start soon')
    event_bus.subscribe_async(handler)


def main():
    c = config.sense_ai
    if len(c.host) == 0:
        logger.error('Config.Senseai.ServerUrl is empty, the senseai service is now exiting')
        return

    try:
        dckr_mngr = DockerManager()

        dckr_mngr.run()
        time.sleep(3.)

        register_senseai_service('senseai_service', 'senseai_service-instance', 'The Code Project SenseAi Object Detection and Facial Recognition Service®')

        proc_fr = None
        if c.fr_enabled:
            logger.info('SenseAI Facial Recognition is enabled')
            proc_fr = Process(target=setup_fr, args=())
            proc_fr.daemon = True
            proc_fr.start()
        else:
            logger.warning('SenseAI Facial Recognition is not enabled')

        proc_alpr = None
        if c.alpr_enabled:
            logger.info('SenseAI ALPR is enabled')
            proc_alpr = Process(target=setup_alpr, args=())
            proc_alpr.daemon = True
            proc_alpr.start()
        else:
            logger.warning('SenseAI ALPR is not enabled')

        if c.od_enabled:
            logger.info('SenseAI Object Detection is enabled')
            setup_od()
        else:
            logger.warning('SenseAI Object Detection is not enabled')

        if proc_fr is not None:
            proc_fr.join()
            proc_fr.terminate()

        if proc_alpr is not None:
            proc_alpr.join()
            proc_alpr.terminate()

        logger.warning('SenseAI Service has been ended')
    except BaseException as ex:
        logger.error(f'an error occurred on SenseAI Service main function, ex: {ex}')

    logger.warning('SenseAI Service has been ended')


if __name__ == '__main__':
    main()
