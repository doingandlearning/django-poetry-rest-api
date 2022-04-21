from rest_framework import serializers

from actors.models import Actor
from .models import Show


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ("first_name", "last_name")


class ShowSerializer(serializers.ModelSerializer):
    """ Serializer of a show """

    star = ActorSerializer()

    class Meta:
        model = Show
        fields = '__all__'

    def create(self, data):
        star_data = data.pop("star")

        show = Show(**data)
        show.star, _created = Actor.objects.get_or_create(**star_data)
        show.save()
        return show

    def update(self, show, data):
        star_data = data.pop("star")

        show.title = data.get('title', show.title)
        show.image = data.get('image', show.image)
        show.year = data.get('year', show.year)
        show.number_of_seasons = data.get(
            'number_of_seasons', show.number_of_seasons)
        show.worth_a_watch = data.get('worth_a_watch', show.worth_a_watch)

        if star_data:
            show.star, _created = Actor.objects.get_or_create(**star_data)

        show.save()
        return show
