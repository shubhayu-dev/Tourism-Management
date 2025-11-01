from django.db import models

class Package(models.Model):
    name = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    duration_days = models.IntegerField()

    def __str__(self):
        return self.name
