from django.db import models
from django.contrib.auth.models import User

def get_common_name(self):
	return "%s %s" % (self.first_name, self.last_name) if self.first_name and self.last_name else self.username

User.add_to_class("__str__", get_common_name)
