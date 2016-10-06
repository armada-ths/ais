from uuid import uuid4
from PIL import Image, ImageFile
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.deconstruct import deconstructible
import os


# Hack for making pillow accept large images
# (should maybe be removed after importing images)
ImageFile.SAFEBLOCK = 1024*10000


def path():
    pass


# Check if a thumbnail should be generated or not
# Based on original image uploaded with uuid
# and generated image having the same name
def should_generate(original, generated):
    if original:
        if generated is None:
            return True
        else:
            original_name, _ = os.path.splitext(original.name)
            generated_name, _ = os.path.splitext(generated.name)
            if original_name is not generated_name:
                return True
    return False


# Intended to be used as an argument for upload_to option in ImageField.
# To create a callable: upload_to = UploadToDirUUID('path','to','dir')
# Generates a random filename for an image in the specified directories
# formatted as 'MEDIA_ROOT/<args[0]>/.../<random id>.<ext>'
# The path keeps the file extension of the input file
@deconstructible
class UploadToDirUUID(object):
    path = '{}/{}{}'

    def __init__(self, *args):
        self.directory = '/'.join(args)

    def __call__(self, instance, filename):
        _, ext = os.path.splitext(filename)
        random_id = uuid4().hex
        return UploadToDirUUID.path.format(self.directory, random_id, ext)


@deconstructible
class UploadToDir(object):
    path = '{}/{}'

    def __init__(self, *args):
        self.directory = '/'.join(args)

    def __call__(self, instance, filename):
        return UploadToDir.path.format(self.directory, filename)


# Converts the input image to a 256 colors png,
# creates a thumbnail with the specified height and width
# and returns it as a new file
def format_png(filename, width, height):
    img = Image.open(filename)
    img.thumbnail((width, height))
    if img.mode is not 'P':
        img = img.convert('P')
    path, ext = os.path.splitext(filename)
    buf = BytesIO()
    if ext != '.png':
        filename = path + '.png'
    img.save(buf, 'png')
    return SimpleUploadedFile(
        filename,
        buf.getvalue(),
        'image/png')


# Creates a jpeg thumbnail of the input image
# and returns it as a new file
def format_jpg(filename, width, height):
    img = Image.open(filename)
    img.thumbnail((width, height))
    if img.mode is 'P':
        img = img.convert('RGB')
    path, ext = os.path.splitext(filename)
    buf = BytesIO()
    if ext != '.jpg':
        filename = path + '.jpg'
    img.save(buf, 'jpeg', quality=80, optimize=True)
    return SimpleUploadedFile(
        filename,
        buf.getvalue(),
        'image/jpeg')
