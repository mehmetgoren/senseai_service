import os
from os.path import isfile, join

import requests

from common.utilities import logger
from core_fr.models.face_list_response import FaceListResponse
from utils.dir import create_dir_if_not_exists
from utils.json_serializer import deserialize_json
from utils.utilities import get_module_url, get_train_dir_path


class FaceTrainer:
    def __init__(self):
        self.url = get_module_url('v1/vision/face/recognize')
        self.folder_path = get_train_dir_path()
        create_dir_if_not_exists(self.folder_path)

    def fit(self):
        list_addr = get_module_url('v1/vision/face/list')
        faces_response_json = requests.post(list_addr).text
        faces: FaceListResponse = FaceListResponse()
        deserialize_json(faces_response_json, faces)

        if not faces.success:
            logger.error(f'an error occurred while getting face list, error: {faces.err_trace}')
            return
        if faces.faces is not None and len(faces.faces) != 0:
            delete_addr = get_module_url('v1/vision/face/delete')
            for name in faces.faces:
                try:
                    requests.post(delete_addr, data={'userid': name})
                except BaseException as ex:
                    logger.error(f'en error occurred while deleting a SenseAI face, ex: {ex}')

        register_addr = get_module_url('v1/vision/face/register')
        for dir_name in os.listdir(self.folder_path):
            full_path_dir = join(self.folder_path, dir_name)
            files_paths = os.listdir(full_path_dir)
            files: dict = {}
            for index, image_path in enumerate(files_paths):
                full_path_file = join(full_path_dir, image_path)
                if isfile(full_path_file):
                    files[f'image{index + 1}'] = open(full_path_file, 'rb').read()
            if len(files) > 0:
                requests.post(register_addr, files=files, data={'userid': dir_name})
                # file_dic['userid'] = dir_name
                # requests.post(register_addr, data=file_dic)
