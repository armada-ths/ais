from django.db import models
from lib.image import UploadToDir


class Building(models.Model):
    name = models.CharField(max_length=50, blank=False)
    map_image = models.ImageField(
        upload_to=UploadToDir('building'),
        blank=False
    )

    def __str__(self):
        return self.name


class Room(models.Model):
    name = models.CharField(max_length=80, blank=True)
    floor = models.PositiveSmallIntegerField(default=0, blank=False)
    building = models.ForeignKey(Building)

    def __str__(self):
        if self.name:
            return "{} > Floor {} > {}".format(self.building.name, self.floor, self.name)
        return "{} > Floor {}".format(self.building.name, self.floor)


class Location(models.Model):
    x_pos = models.FloatField(default=0.0, blank=False)
    y_pos = models.FloatField(default=0.0, blank=False)
    room = models.ForeignKey(Room)

    def __str__(self):
        return str(self.room)
