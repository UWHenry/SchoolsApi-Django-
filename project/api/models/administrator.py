from django.db import models

from .school import School

class Administrator(models.Model):
    name = models.CharField(max_length=128, blank=False, null=False)
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=False, null=False)


    def __str__(self):
        return self.name