from django.db import models

# Create your models here.


class Actor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_year = models.IntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
