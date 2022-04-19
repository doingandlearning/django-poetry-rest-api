from rest_framework import serializers

from actors.models import Actor
from .models import Show


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ("first_name", "birth_year")


class ShowSerializer(serializers.ModelSerializer):
    """ Serializer of a show """

    star = ActorSerializer()

    class Meta:
        model = Show
        fields = '__all__'
