from django.db import models

# Create your models here.
class Car(models.Model):
    name = models.CharField(max_length=32)
    category = models.CharField(max_length=32)

    class Meta:
        unique_together = ("name", "category")
    
    def __str__(self):
        return self.name;


class Time(models.Model):
    time = models.IntegerField()
    profile = models.CharField(max_length=16)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    track = models.CharField(max_length=32)
    mode = models.CharField(max_length=32)
    
    class Meta:
        unique_together = ("time", "profile", "car", "track", "mode")
    
    @property
    def strtime(self):
        ms = self.time
        sc = (ms - (ms % 1000)) / 1000
        ms = ms % 1000
        mn = (sc - (sc % 60)) / 60
        sc = sc % 60
        return "{:02d}:{:02d}.{:03d}".format(int(mn), int(sc), int(ms))

