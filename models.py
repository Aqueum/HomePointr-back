from django.db import models


class Provider(models.Model):
    name = models.CharField(max_length=127)

    def __str__(self):
        return self.provider_name


class PropetyType(models.Model):
    ptype = models.CharField(max_length=31)

    def __str__(self):
        return self.property_type


class Council(models.Model):
    name = models.CharField(max_length=127)

    def __str__(self):
        return self.council_name


class Support(models.Model):
    support = models.CharField(max_length=31)

    def __str__(self):
        return self.property_type


class Property(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    ptype = models.ForeignKey(PropetyType)
    name = models.CharField(max_length=255)
    address1 = models.CharField(max_length=255, default=name)
    address2 = models.CharField(max_length=255)
    address3 = models.CharField(max_length=255)
    town = models.CharField(max_length=31)
    region = models.CharField(max_length=31)
    postcode = models.CharField(max_length=31)
    lat = models.DecimalField(max_digits=8, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)
    council = models.ForeignKey(Council)
    bedrooms = models.IntegerField(default=1)
    beds = models.IntegerField(default=1)
    max_occupants = models.IntegerField(default=1)
    support = models.ManyToManyField(Support)
    wheelchair_accessible = models.BooleanField
    parking = models.BooleanField
    shared = models.BooleanField
    rent_pcm = models.DecimalField(max_digits=7, decimal_places=2)
    deposit = models.DecimalField(max_digits=7, decimal_places=2)
    units = models.IntegerField(default=1)
    next_available = models.DateField

    def __str__(self):
        return self.property_name


class Photo(models.Model):
    prop = models.ForeignKey(Property, on_delete=models.CASCADE)
    url = models.CharField(max_length=200)
    credit = models.CharField(max_length=200)
    description = models.CharField(max_length=800)

    def __str__(self):
        return self.photo_description
