import os

from django.core.files.storage import FileSystemStorage
from rest_framework.exceptions import NotFound
from django.conf import settings


def delete_file(name, url):
    fs = FileSystemStorage(
        location=os.path.join(settings.MEDIA_ROOT, url), base_url=os.path.join(settings.MEDIA_URL, url)
    )

    name = fs.path(name)
    try:
        if os.path.isdir(name):
            os.rmdir(name)
        else:
            os.remove(name)
    except FileNotFoundError as e:
        raise NotFound() from e


def add_file(file, url):
    fs = FileSystemStorage(
        location=os.path.join(settings.MEDIA_ROOT, url), base_url=os.path.join(settings.MEDIA_URL, url)
    )
    file_url = fs.save(file.name, file)
    file_url = fs.url(file_url)
    return file_url


def move_file(file, url_source, url_destination):
    add_file(file, url_destination)
    delete_file(file.name, url_source)
