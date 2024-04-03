from os import path
from typing import List, Any
import docker
from docker.types import Mount

from common.config import SenseAiImage
from common.utilities import config, logger
from utils.dir import get_root_path_for_senseai, create_dir_if_not_exists


# for more info: https://docker-py.readthedocs.io/en/stable/containers.html
class DockerManager:
    def __init__(self):
        self.client = docker.from_env()
        self.container_name = 'senseai-server'
        self.sense_ai_config = config.sense_ai

    def __get_image_name(self) -> str:
        docker_type = self.sense_ai_config.image
        if docker_type == SenseAiImage.CPU:
            return 'codeproject/ai-server'
        elif docker_type == SenseAiImage.GPU_CUDA_11_7:
            return 'codeproject/ai-server:cuda11_7'
        elif docker_type == SenseAiImage.GPU_CUDA_12_2:
            return 'codeproject/ai-server:cuda12_2'
        elif docker_type == SenseAiImage.ARM64:
            return 'codeproject/ai-server:arm64'
        elif docker_type == SenseAiImage.RPI64:
            return 'codeproject/ai-server:rpi64'
        else:
            return 'codeproject/ai-server'

    def __init_container(self, all_containers: List):
        for container in all_containers:
            if container.name == self.container_name:
                if container.status == 'running':
                    logger.warning(f'a running SenseAI server container has been found. No need to create a new one.')
                    return container
                else:
                    container.start()
                    logger.warning(f'a stopped SenseAI server container has been found and started.')
                    return container
                # self.stop_and_remove_container(container)
                # logger.warning(f'a previous SenseAI server container has been found and removed.')
                # break

        environments = dict()
        docker_image = self.sense_ai_config.image
        is_cuda = docker_image == SenseAiImage.GPU_CUDA_11_7 or docker_image == SenseAiImage.GPU_CUDA_12_2
        device_requests = []
        if is_cuda:
            device_requests.append(docker.types.DeviceRequest(count=-1, capabilities=[['gpu']]))

        mounts = list()
        mount_dir_path = path.join(get_root_path_for_senseai(config), 'senseai')

        data_dir_path = path.join(mount_dir_path, 'data')
        create_dir_if_not_exists(data_dir_path)
        mounts.append(Mount(source=f'{data_dir_path}', target='/etc/codeproject/ai', type='bind'))

        modules_dir_path = path.join(mount_dir_path, 'modules')
        create_dir_if_not_exists(modules_dir_path)
        mounts.append(Mount(source=f'{modules_dir_path}', target='/app/modules', type='bind'))

        image_name = self.__get_image_name()
        logger.warning(f'creating a new SenseAI server container with image: {image_name}, please be patient, it may take a while...')
        container = self.client.containers.run(image=image_name, detach=True, restart_policy={'Name': 'unless-stopped'},
                                               name=self.container_name, ports={'32168': str(self.sense_ai_config.port)},
                                               environment=environments, mounts=mounts, device_requests=device_requests)
        logger.warning(f'a new SenseAI server container({image_name}) has been created successfully.')
        # environment=environments, mounts=mounts, device_requests=device_requests,
        # runtime='nvidia' if is_cuda else '')
        return container

    def run(self) -> Any:
        all_containers = self.get_all_containers()
        container = self.__init_container(all_containers)
        return container

    # def remove(self):
    #     container = self.get_container(self.container_name)
    #     if container is not None:
    #         self.stop_and_remove_container(container)

    def stop(self):
        container = self.get_container(self.container_name)
        if container is not None:
            container.stop()

    def get_container(self, container_name: str):
        filters: dict = {'name': container_name}
        containers = self.client.containers.list(filters=filters)
        return containers[0] if len(containers) > 0 else None

    def get_all_containers(self):
        return self.client.containers.list(all=True)

    # @staticmethod
    # def stop_and_remove_container(container):
    #     container.stop()
    #     container.remove()
