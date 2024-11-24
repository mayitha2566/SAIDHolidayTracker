
from django.db import models

class SAID(models.Model):
    id_number = models.CharField(max_length=13, unique=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    is_citizen = models.BooleanField()
    search_count = models.IntegerField(default=1)

    def __str__(self):
        return self.id_number

class Holiday(models.Model):
    said = models.ForeignKey(SAID, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    type = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} on {self.date}"