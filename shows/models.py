from django.db import models

from actors.models import Actor
from creators.models import Creator


class Show(models.Model):
    """
    A 90s TV show
    """
    title = models.CharField(
        max_length=50, default=None)  # fields are required by default so no need to specify
    image = models.CharField(max_length=250, default=None)

    # must be positive number, integerfield can be negative
    year = models.PositiveIntegerField(default=None)
    number_of_seasons = models.PositiveIntegerField(default=None)
    worth_a_watch = models.BooleanField(default=True, null=True)

    star = models.ForeignKey(
        Actor, on_delete=models.SET_NULL, null=True, related_name="starred")

    creator = models.ForeignKey(
        Creator, null=True, blank=True, on_delete=models.SET_NULL, related_name="creations")

    supporting_actors = models.ManyToManyField(
        Actor, blank=True, related_name="supported")

    def __str__(self):
        """Formats entries in the Admin panel"""
        return f"{self.title} - {self.year}"
