from django.db import models
from django.contrib.auth.models import Group
from fair.models import Fair

# Create your models here.

Group.add_to_class('is_role', models.BooleanField(default=False))

Group.add_to_class('fair', models.ForeignKey(Fair, null=True))

