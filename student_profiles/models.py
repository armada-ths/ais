from django.db import models

class StudentProfile(models.Model):
    '''
    A striped down version of a user profile
    Is used by api and banquet apps
    '''
    nickname = models.CharField(max_length=100)

    def __str__(self):
        return self.nickname
