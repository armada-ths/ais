from django.db import models
from django.contrib.auth.models import Group
# Create your models here.

Group.add_to_class('is_role', models.BooleanField(default=False))
