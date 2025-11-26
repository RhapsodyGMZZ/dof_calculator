from django.db import models

class Sensor(models.Model):
    name = models.CharField(max_length=100)
    crop_factor = models.FloatField()
    coc = models.FloatField()  # Circle of Confusion in mm
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']