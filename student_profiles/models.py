from django.db import models

# Create your models here.
class StudentProfile(models.Model):
	nickname = models.CharField(max_length=100)

	def __str__(self):
		return self.nickname
