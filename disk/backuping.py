from os.path import join

import yadisk
import pandas as pd

from settings import ya_token
from settings import local_data_path, disk_data_path, data_file
from settings import local_photo_path, disk_photo_path


class Disk:

    def __init__(self):

        self.ya = yadisk.YaDisk(token=ya_token)
        if not self.ya.check_token():
            raise ValueError("Неправильный токен для Я.Диска")

    def save_file(self, src, dst, file, overwrite=True):
        self.ya.upload(join(src, file), join(dst, file), overwrite=overwrite)

    def save_data(self):
        self.save_file(local_data_path, disk_data_path, data_file)

    def save_photo(self, photo):
        self.save_file(local_photo_path, disk_photo_path, photo)

    def save_object(self, data):
        self.save_data()
        if "photo" in data:
            self.save_photo(data["photo"])


disk = Disk()
