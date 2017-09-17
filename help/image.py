'''
This file was created to ease testing ImageField

Feel free to use and expand this.

by Grigory Glukhov
'''
   
import os.path
from django.core.files.uploadedfile import SimpleUploadedFile
 
__all__ = ('loadTestImage')

def loadTestImage():
    return SimpleUploadedFile(name='test_image.jpg', content=open(TEST_IMAGE_PATH, 'rb').read(), content_type='image/jpeg')

TEST_IMAGE_PATH=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_image.jpg')
