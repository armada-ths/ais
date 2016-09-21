from uuid import uuid4
# from PIL import Image


# Intended to be used as an argument for upload_to option in ImageField
# Generates a random path for an image formatted as
# 'MEDIA_ROOT/<args[0]>/.../<random id>.<ext>'
# The path keeps the file extension of the input file
def random_path(*args):
    def path(instance, filename):
        directory = '/'.join(args)
        ext = filename.split('.')[-1]
        random_id = uuid4().hex
        return '{}/{}.{}'.format(directory, random_id, ext)
    return path


def optimize_png(filename):
    return


def optimize_jpg(filename):
    return
