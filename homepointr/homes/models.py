from django.db import models


class Grain(models.Model):
    name = models.CharField(max_length=127)

    def __str__(self):
        return self.name


class Bread(models.Model):
    name = models.CharField(max_length=127)
    grain = models.ForeignKey(Grain)

    def __str__(self):
        return self.name
