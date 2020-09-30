from enum import Enum


class ImageUploadInfo(Enum):
    URL = 'images' + '/'
    TYPE = ['jpg', 'png', 'jpeg']
    LIMIT_SIZE = 2 * 1024 * 1024


class CSVUploadInfo(Enum):
    LIMIT_SIZE = 2 * 1024 * 1024
