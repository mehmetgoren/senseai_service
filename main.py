import sys
import time
from multiprocessing import Process
from typing import List

from common.data.ai_module_model import AiModuleModel
from common.data.ai_module_repository import AiModuleRepository
from core.detector import Detector
from core.read_service_event_handler import ReadServiceEventHandler
from docker_manager import DockerManager

from common.event_bus.event_bus import EventBus
from common.utilities import config, logger, crate_redis_connection, RedisDb
from core_fr.train_event_handler import TrainEventHandler
from utils.utilities import EventChannels, register_senseai_service


def setup_fr_train():
    logger.info('SenseAI face training event handler will start soon')
    eb = EventBus(EventChannels.face_train_request)
    th = TrainEventHandler()
    eb.subscribe_async(th)


def check_sense_ai_default_modules() -> List[AiModuleModel]:
    redis_conn = None
    try:
        redis_conn = crate_redis_connection(RedisDb.MAIN)
        ai_module_rep = AiModuleRepository(crate_redis_connection(RedisDb.MAIN))
        ret = ai_module_rep.check_sense_ai_default_modules()
    finally:
        if redis_conn is not None:
            redis_conn.close()
    return ret


def setup(module: AiModuleModel):
    # todo: change snapshot_service to work with new dictionary key. It must behave like a proxy
    channel = EventChannels.snapshot_in if module.motion_detection_enabled else EventChannels.read_service
    logger.info(f'{module.name} event handler channel: {channel}')
    event_bus = EventBus(channel)

    detector = Detector(module)
    handler = ReadServiceEventHandler(detector)

    logger.info(f'SenseAI service will start soon for {module.name}')

    while True:
        try:
            event_bus.subscribe_async(handler)
            break
        except BaseException as ex:
            logger.error(f'an error occurred while subscribing to event bus, ex: {ex}')
            time.sleep(3)
    sys.exit()


def main():
    if len(config.sense_ai.host) == 0:
        logger.error('Config.Senseai.ServerUrl is empty, the senseai service is now exiting')
        return

    modules: List[AiModuleModel] = check_sense_ai_default_modules()
    procs = []
    # dckr_mngr = None
    try:
        dckr_mngr = DockerManager()

        dckr_mngr.run()
        time.sleep(3.)

        register_senseai_service('senseai_service', 'senseai_service-instance', 'The Code Project SenseAi Object Detection and Facial Recognition Service®')

        for module in modules:
            if module.enabled:
                logger.info(f'{module.name} is enabled')
                proc = Process(target=setup, args=(module,))
                procs.append(proc)
                proc.daemon = True
                proc.start()
            else:
                logger.warning(f'{module.name} is not enabled')

        setup_fr_train()

        logger.warning('SenseAI Service has been ended')
    except BaseException as ex:
        logger.error(f'an error occurred on SenseAI Service main function, ex: {ex}')
    finally:
        for proc in procs:
            try:
                # proc.join()
                proc.terminate()
            except BaseException as ex:
                logger.error(f'an error occurred while terminating a process, ex: {ex}')
        # if dckr_mngr is not None:
        #     dckr_mngr.stop()

    logger.warning('SenseAI Service has been ended')


if __name__ == '__main__':
    main()
