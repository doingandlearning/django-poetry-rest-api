from django.db import models

# Create your models here.


class Creator(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    website = models.URLField(null=True, blank=True)
    birth_year = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
