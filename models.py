from django.db import models


class Provider(models.Model):
    provider_name = models.CharField(max_length=200)

    def __str__(self):
        return self.provider_name


class Property(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    property_name = models.CharField(max_length=200)
    bedrooms = models.IntegerField(default=1)

    def __str__(self):
        return self.property_name


class Photo(models.Model):
    prop = models.ForeignKey(Property, on_delete=models.CASCADE)
    photo_url = models.CharField(max_length=200)
    photo_credit = models.CharField(max_length=200)
    photo_description = models.CharField(max_length=800)

    def __str__(self):
        return self.photo_description
