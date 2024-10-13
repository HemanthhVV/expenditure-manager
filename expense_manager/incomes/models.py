from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
# Create your models here.

class Income(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=now)
    description = models.TextField()
    owner = models.ForeignKey(to=User,on_delete=models.CASCADE)
    source = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.source + " " + self.description

    class Meta:
        ordering : ['-date']

class Source(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Sources"
    def __str__(self) -> str:
        return self.name