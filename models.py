from django.db import models


class Provider(models.Model):
    provider_name = models.CharField(max_length=200)

    def __str__(self):
        return self.provider_name


class Council(models.Model):
    council_name = models.CharField(max_length=200)

    def __str__(self):
        return self.council_name


class PropetyType(models.Model):
    property_type = models.CharField(max_length=20)

    def __str__(self):
        return self.property_type


class Support(models.Model):
    property_type = models.CharField(max_length=20)

    def __str__(self):
        return self.property_type


class Property(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    property_type = models.ForeignKey(PropetyType)
    property_name = models.CharField(max_length=200)
    bedrooms = models.IntegerField(default=1)
    beds = models.IntegerField(default=1)
    max_occupants = models.IntegerField(default=1)
    rent_pcm = models.DecimalField(decimal_places=2, default=0.00)
    deposit = models.DecimalField(decimal_places=2, default=0.00)
    parking = models.BooleanField
    shared = models.BooleanField
    support = models.ManyToManyField(Support)
    wheelchair_accessible = models.BooleanField
    council = models.ForeignKey(Council)

    def __str__(self):
        return self.property_name


class Photo(models.Model):
    prop = models.ForeignKey(Property, on_delete=models.CASCADE)
    photo_url = models.CharField(max_length=200)
    photo_credit = models.CharField(max_length=200)
    photo_description = models.CharField(max_length=800)

    def __str__(self):
        return self.photo_description
