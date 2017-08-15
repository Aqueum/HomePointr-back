from django.db import models


class Bread(models.Model):
    name = models.CharField(max_length=127)

    def __str__(self):
        return self.name