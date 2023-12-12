from django.db import models

class Airport(models.Model) :
    icao_code = models.CharField(max_length=4)
    airport_name = models.CharField(max_length=255)
    airport_country = models.CharField(max_length=2)
    airport_latitude = models.FloatField(default=0)
    airport_longitude = models.FloatField(default=0)
    airport_elevation = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self) :
        return f'{self.icao_code} | {self.airport_name}'
# Create your models here.
