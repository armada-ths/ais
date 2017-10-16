from uuid import uuid4
from PIL import Image, ImageFile
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.deconstruct import deconstructible
import os, shutil
from django.conf import settings


MEDIA_ROOT = settings.MEDIA_ROOT


# Hack for making pillow accept large images
# (should maybe be removed after importing images)
ImageFile.SAFEBLOCK = 1024*10000


def path():
    pass


def resize_and_save_image(image, directory, width, height, extension):
    '''
    Creates a copy of image in provided directory (same parent directory as the file) if necessary and saves it.
    '''
    if os.path.isfile(image.path):
        path = os.path.join(os.path.dirname(os.path.dirname(image.path)), directory, os.path.basename(image.name))
        if not os.path.isfile(image.path):
            shutil.copyfile(image.path, path)
            return format_image(path, width, height, extension)
    return image


# Updates an imagefield that is linked to another image
# Resizes the image and converts it to another format as specified
def update_image_field(original, image, width, height, convert_to):
    if should_generate(original, image):
        if image:
            os.remove(os.path.join(MEDIA_ROOT, image.name))
        path = os.path.join(MEDIA_ROOT, original.name)
        return format_image(path, width, height, convert_to)
    return image


# Check if a thumbnail should be generated or not
# Based on original image uploaded with uuid
# and generated image having the same name
def should_generate(original, generated):
    if original:
        if generated is None:
            return True
        else:
            original_name, _ = os.path.splitext(os.path.basename(original.name))
            generated_name, _ = os.path.splitext(os.path.basename(generated.name))
            if original_name != generated_name:
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


# Wrapper of the image format functions
def format_image(filename, width, height, img_type):
    if img_type == 'png':
        return format_png(filename, width, height)
    if img_type == 'jpg':
        return format_jpg(filename, width, height)


# Converts the input image to a 256 colors png,
# creates a thumbnail with the specified height and width
# and returns it as a new file
def format_png(filename, width, height):
    img = Image.open(filename)
    img.thumbnail((width, height))
    if img.mode != 'P':
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
    if img.mode == 'P':
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

def load_test_image():
    return SimpleUploadedFile(name='test_image.jpg', content=open(TEST_IMAGE_PATH, 'rb').read(), content_type='image/jpeg')

TEST_IMAGE_PATH=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_image.jpg')
